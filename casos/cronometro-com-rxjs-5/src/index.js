import Rx from "rxjs";

const durationRange = document.getElementById("durationRange");
const duration$ = Rx.Observable.fromEvent(durationRange, "input").map(_e => ({
  duration: durationRange.value
}));

const resetButton = document.getElementById("resetButton");
const reset$ = Rx.Observable.fromEvent(resetButton, "click");

const count$ = reset$.startWith(0).switchMap(t => {
  return Rx.Observable.interval(1000).map(count => ({ elapsed: count }));
});

const event$ = Rx.Observable.merge(duration$, count$);

const gaugeProgress = document.getElementById("gaugeProgress");
const ellapsedTime = document.getElementById("ellapsedTime");

const cronometro$ = event$
  .startWith({
    duration: 100,
    elapsed: 0
  })
  .scan((state, curr) => ({ ...state, ...curr }), {});

const render = state => {
  console.log(JSON.stringify({ state }));
  const percent = Number.parseInt((state.elapsed / state.duration) * 100, 10);
  gaugeProgress.max = state.duration;
  gaugeProgress.value = state.elapsed;
  gaugeProgress.innerHTML = `${percent}%`;
  ellapsedTime.innerHTML = `${percent}%`;
  durationRange.value = state.duration;
};

cronometro$.subscribe(render);
