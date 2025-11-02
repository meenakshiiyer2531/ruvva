import { describe, it, expect } from '@jest/globals';

// Lightweight pure scoring helpers extracted inline from Assessment component logic
const QUESTIONS_PER_AXIS = 5;
const RIASEC_AXES = ["Realistic","Investigative","Artistic","Social","Enterprising","Conventional"];

function computePercentScores(answers){
  const axisScores = answers.reduce((acc, cur)=>{ acc[cur.axis] = (acc[cur.axis]||0)+cur.score; return acc; },{});
  const maxPerAxis = QUESTIONS_PER_AXIS*2;
  return RIASEC_AXES.map(axis=>({axis, raw: axisScores[axis]||0, percent: Math.round(((axisScores[axis]||0)/maxPerAxis)*100)}));
}

describe('RIASEC scoring', () => {
  it('computes 0% for empty answers', () => {
    const result = computePercentScores([]);
    result.forEach(r=> expect(r.percent).toBe(0));
  });
  it('computes 100% for full Agree answers on one axis', () => {
    const answers = Array.from({length:QUESTIONS_PER_AXIS}, (_,i)=>({q:i+1, axis:'Realistic', score:2}));
    const result = computePercentScores(answers);
    const realistic = result.find(r=>r.axis==='Realistic');
    expect(realistic.percent).toBe(100);
  });
  it('partial scoring boundary rounding', () => {
    const answers = [
      {q:1, axis:'Artistic', score:2},
      {q:2, axis:'Artistic', score:1},
      {q:3, axis:'Artistic', score:0},
      {q:4, axis:'Artistic', score:2},
      {q:5, axis:'Artistic', score:1},
    ];
    const result = computePercentScores(answers);
    const artistic = result.find(r=>r.axis==='Artistic');
    // raw = 6 max = 10 => 60%
    expect(artistic.raw).toBe(6);
    expect(artistic.percent).toBe(60);
  });
});
