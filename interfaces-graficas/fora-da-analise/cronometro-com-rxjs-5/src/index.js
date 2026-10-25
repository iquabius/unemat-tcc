import Rx from "rxjs";

const durationRange = document.getElementById("durationRange");
const duration$ = Rx.Observable.fromEvent(durationRange, "input").map(_e => ({
  duration: durationRange.value
}));

const resetButton = document.getElementById("resetButton");
const reset$ = Rx.Observable.fromEvent(resetButton, "click").mapTo({
  elapsed: 0
});

const count$ = Rx.Observable.interval(1000).map(_ => ({ count: true }));

const event$ = Rx.Observable.merge(duration$, reset$, count$);

const gaugeProgress = document.getElementById("gaugeProgress");
const ellapsedTime = document.getElementById("ellapsedTime");

const cronometro$ = event$
  .startWith({
    duration: 5,
    elapsed: 0
  })
  .scan((state, curr) => {
    const shouldCount = state.elapsed < state.duration;
    const newElapsed = shouldCount ? state.elapsed + 1 : state.elapsed;
    const newDuration =
      state.duration >= state.elapsed ? state.duration : state.elapsed;
    return curr.count
      ? { ...state, duration: newDuration, elapsed: newElapsed }
      : { ...state, ...curr };
  }, {});

const render = state => {
  const percent = Number.parseInt((state.elapsed / state.duration) * 100, 10);
  gaugeProgress.max = state.duration;
  gaugeProgress.value = state.elapsed;
  gaugeProgress.innerHTML = `${percent}%`;
  ellapsedTime.innerHTML = `${percent}%`;
  durationRange.value = state.duration;
};

cronometro$.subscribe(render);
