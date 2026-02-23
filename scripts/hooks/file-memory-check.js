#!/usr/bin/env node
/**
 * Stop Hook - File Memory Check
 *
 * Checks phase completion status in active task plans
 * and reports progress after each response.
 */

const fs = require('fs');
const path = require('path');

let data = '';

process.stdin.on('data', chunk => {
  data += chunk;
});

process.stdin.on('end', () => {
  try {
    const plansDir = path.join(process.cwd(), '.claude', 'plans');

    if (!fs.existsSync(plansDir)) {
      console.log(data);
      process.exit(0);
    }

    const files = fs.readdirSync(plansDir).filter(f =>
      f.endsWith('.md') && (f.includes('task_plan') || f.startsWith('task_plan'))
    );

    for (const file of files) {
      const filePath = path.join(plansDir, file);
      const content = fs.readFileSync(filePath, 'utf8');

      // Count phase statuses
      const completeCount = (content.match(/\*\*(状态|Status):\*\*\s*complete/gi) || []).length;
      const inProgressCount = (content.match(/\*\*(状态|Status):\*\*\s*in_progress/gi) || []).length;
      const pendingCount = (content.match(/\*\*(状态|Status):\*\*\s*pending/gi) || []).length;
      const totalPhases = completeCount + inProgressCount + pendingCount;

      if (totalPhases > 0) {
        if (pendingCount === 0 && inProgressCount === 0) {
          console.error(`[File-Memory] ${file}: 所有 ${totalPhases} 个阶段已完成。可以使用 /file-memory archive 归档。`);
        } else {
          console.error(`[File-Memory] ${file}: ${completeCount}/${totalPhases} 阶段完成, ${inProgressCount} 进行中, ${pendingCount} 待开始`);
        }
      }
    }
  } catch (_error) {
    // Silently ignore errors
  }

  console.log(data);
});
