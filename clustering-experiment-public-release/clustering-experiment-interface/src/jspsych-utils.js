export class Stopwatch {
  constructor() {
    this.time = null
  }

  start() {
    this.time = performance.now()
  }

  stop() {
    const time = performance.now() - this.time
    this.time = null
    return time
  }
}

export function wait (ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// A more strict parseInt
export function filterInt(value) {
  if (/^[-+]?(\d+|Infinity)$/.test(value)) {
    return Number(value)
  } else {
    return NaN
  }
}
