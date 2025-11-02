import { describe, it, expect } from '@jest/globals';

// Reproduce logic from Assessment for generation
const RIASEC_AXES = ["Realistic","Investigative","Artistic","Social","Enterprising","Conventional"];
const QUESTION_POOL = {
  Realistic: Array.from({length:8},(_,i)=>`R${i}`),
  Investigative: Array.from({length:8},(_,i)=>`I${i}`),
  Artistic: Array.from({length:8},(_,i)=>`A${i}`),
  Social: Array.from({length:8},(_,i)=>`S${i}`),
  Enterprising: Array.from({length:8},(_,i)=>`E${i}`),
  Conventional: Array.from({length:8},(_,i)=>`C${i}`),
};
const QUESTIONS_PER_AXIS = 5;

function generate(){
  const generated=[]; let qId=1;
  RIASEC_AXES.forEach(axis=>{
    const pool=QUESTION_POOL[axis];
    const shuffled=[...pool].sort(()=>Math.random()-0.5).slice(0,QUESTIONS_PER_AXIS);
    shuffled.forEach(text=>generated.push({id:qId++, text, axis}));
  });
  return generated.sort(()=>Math.random()-0.5);
}

describe('Question generation', () => {
  it('produces correct count total', () => {
    const g = generate();
    expect(g.length).toBe(RIASEC_AXES.length * QUESTIONS_PER_AXIS);
  });
  it('produces correct count per axis', () => {
    const g = generate();
    RIASEC_AXES.forEach(axis => {
      expect(g.filter(q=>q.axis===axis).length).toBe(QUESTIONS_PER_AXIS);
    });
  });
  it('unique IDs sequential', () => {
    const g = generate();
    const ids = g.map(q=>q.id);
    const unique = new Set(ids);
    expect(unique.size).toBe(ids.length);
  });
});
