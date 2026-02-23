#!/usr/bin/env node
/**
 * SessionStart Hook - File Memory Init
 *
 * Detects active task plans in .claude/plans/ and outputs
 * a reboot prompt with the 5-Question Reboot Test.
 */

const fs = require('fs');
const path = require('path');
const { log } = require('../lib/utils');

function findActivePlans(plansDir) {
  if (!fs.existsSync(plansDir)) return [];

  const files = fs.readdirSync(plansDir).filter(f => f.endsWith('.md'));
  const activePlans = [];

  for (const file of files) {
    const filePath = path.join(plansDir, file);
    const content = fs.readFileSync(filePath, 'utf8');

    // Check if this is a task_plan file with active (non-complete) phases
    if (content.includes('## 阶段列表') || content.includes('## Phases')) {
      const hasInProgress = /\*\*状态:\*\*\s*in_progress|\*\*Status:\*\*\s*in_progress/i.test(content);
      const hasPending = /\*\*状态:\*\*\s*pending|\*\*Status:\*\*\s*pending/i.test(content);

      if (hasInProgress || hasPending) {
        // Extract goal
        const goalMatch = content.match(/## 目标\s*\n([^\n]+)|## Goal\s*\n([^\n]+)/);
        const goal = goalMatch ? (goalMatch[1] || goalMatch[2] || '').trim() : '未知';

        // Extract current phase
        const phaseMatch = content.match(/## 当前阶段\s*\n([^\n]+)|## Current Phase\s*\n([^\n]+)/);
        const currentPhase = phaseMatch ? (phaseMatch[1] || phaseMatch[2] || '').trim() : '未知';

        activePlans.push({
          file: filePath,
          name: file,
          goal,
          currentPhase,
          hasInProgress
        });
      }
    }
  }

  return activePlans;
}

function main() {
  // Check .claude/plans/ in current working directory
  const plansDir = path.join(process.cwd(), '.claude', 'plans');
  const activePlans = findActivePlans(plansDir);

  if (activePlans.length === 0) {
    // No active plans, silent exit
    process.exit(0);
  }

  log('[File-Memory] 检测到活跃任务计划:');

  for (const plan of activePlans) {
    log(`  - ${plan.name}`);
    log(`    目标: ${plan.goal}`);
    log(`    当前阶段: ${plan.currentPhase}`);
  }

  log('');
  log('[File-Memory] 5 问题重启测试 — 请读取以下文件恢复上下文:');

  for (const plan of activePlans) {
    const baseName = plan.name.replace('task_plan', '').replace('.md', '');
    const findingsFile = path.join(plansDir, `findings${baseName}.md`);
    const progressFile = path.join(plansDir, `progress${baseName}.md`);

    log(`  1. ${plan.file} (我在哪里？目标是什么？)`);
    if (fs.existsSync(findingsFile)) {
      log(`  2. ${findingsFile} (我学到了什么？)`);
    }
    if (fs.existsSync(progressFile)) {
      log(`  3. ${progressFile} (我做了什么？)`);
    }
  }

  log('');
  log('[File-Memory] 建议: 读取上述文件后再继续工作。');

  process.exit(0);
}

main();
