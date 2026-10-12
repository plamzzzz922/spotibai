(function () {
  var root = document.querySelector(".player");
  if (!root) return;

  var duration = parseInt(root.dataset.duration, 10) || 0;
  var button = document.getElementById("toggle");
  var fill = document.getElementById("bar-fill");
  var elapsedEl = document.getElementById("elapsed");
  var bar = root.querySelector(".bar");
  var audio = root.dataset.audio ? new Audio(root.dataset.audio) : null;
  var seconds = 0;
  var timer = null;
  var playing = false;

  function format(total) {
    var m = Math.floor(total / 60);
    var s = Math.floor(total % 60);
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function render(current) {
    elapsedEl.textContent = format(current);
    var pct = duration ? Math.min(100, (current / duration) * 100) : 0;
    fill.style.width = pct + "%";
    bar.setAttribute("aria-valuenow", String(Math.round(pct)));
  }

  function pause() {
    playing = false;
    button.classList.remove("is-playing");
    button.setAttribute("aria-label", "Play");
    if (audio) audio.pause();
    if (timer) { clearInterval(timer); timer = null; }
  }

  function finish() {
    pause();
    seconds = 0;
    render(0);
  }

  function tick() {
    seconds += 1;
    if (seconds >= duration) { finish(); return; }
    render(seconds);
  }

  function play() {
    playing = true;
    button.classList.add("is-playing");
    button.setAttribute("aria-label", "Pause");
    if (audio) {
      audio.play();
    } else {
      // No audio file on this song, so the progress bar is simulated.
      timer = setInterval(tick, 1000);
    }
  }

  if (audio) {
    audio.addEventListener("timeupdate", function () { render(audio.currentTime); });
    audio.addEventListener("ended", finish);
  }

  button.addEventListener("click", function () {
    if (playing) { pause(); } else { play(); }
  });
})();
