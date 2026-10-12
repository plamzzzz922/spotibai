(function () {
  var LIKES_KEY = "tunes.likes";
  var RECENT_KEY = "tunes.recent";
  var DEFAULT_LIKES = [1, 2, 3, 4, 5, 6];

  // No database: likes and recent plays live in this browser's localStorage.
  function read(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      if (raw === null) return fallback.slice();
      var value = JSON.parse(raw);
      return Array.isArray(value) ? value : fallback.slice();
    } catch (error) {
      return fallback.slice();
    }
  }

  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (error) { /* storage blocked */ }
  }

  function likes() { return read(LIKES_KEY, DEFAULT_LIKES); }
  function recent() { return read(RECENT_KEY, []); }

  function renderStars() {
    var liked = likes();
    document.querySelectorAll("[data-like]").forEach(function (button) {
      var id = parseInt(button.dataset.like, 10);
      var on = liked.indexOf(id) !== -1;
      var name = button.dataset.title || "this song";
      button.classList.toggle("on", on);
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.setAttribute(
        "aria-label",
        (on ? "Remove " + name + " from" : "Add " + name + " to") + " liked songs"
      );
    });
  }

  // Shows the right cards, in the right order, inside [data-collection="liked"|"recent"].
  function renderCollections() {
    document.querySelectorAll("[data-collection]").forEach(function (box) {
      var ids = box.dataset.collection === "liked" ? likes() : recent();
      var limit = parseInt(box.dataset.limit || "0", 10);
      var cards = {};
      box.querySelectorAll(".card").forEach(function (card) {
        card.classList.remove("is-shown");
        cards[card.dataset.songId] = card;
      });
      var shown = 0;
      ids.forEach(function (id) {
        var card = cards[String(id)];
        if (card && (!limit || shown < limit)) {
          box.appendChild(card);
          card.classList.add("is-shown");
          shown += 1;
        }
      });
      var scope = box.closest("section") || box.parentElement;
      var empty = scope.querySelector("[data-empty]");
      if (empty) empty.hidden = shown > 0;
    });
  }

  function renderMiniPlayer() {
    var mini = document.getElementById("mini-player");
    var data = document.getElementById("songs-data");
    if (!mini || !data) return;
    var songs = JSON.parse(data.textContent);
    var ids = recent();
    var song = null;
    for (var i = 0; i < ids.length && !song; i += 1) {
      song = songs.filter(function (s) { return s.id === ids[i]; })[0] || null;
    }
    if (!song) { mini.hidden = true; return; }
    document.getElementById("mini-title").textContent = song.title;
    document.getElementById("mini-artist").textContent = "By: " + song.artist;
    var link = document.getElementById("mini-link");
    link.href = mini.dataset.urlTemplate.replace("/0/", "/" + song.id + "/");
    link.setAttribute("aria-label", "Open player for " + song.title);
    mini.hidden = false;
  }

  function renderAll() {
    renderStars();
    renderCollections();
    renderMiniPlayer();
  }

  // Opening a song's player page counts as playing it.
  var player = document.querySelector(".player[data-song-id]");
  if (player) {
    var playedId = parseInt(player.dataset.songId, 10);
    var history = recent().filter(function (id) { return id !== playedId; });
    history.unshift(playedId);
    write(RECENT_KEY, history.slice(0, 20));
  }

  document.addEventListener("click", function (event) {
    var star = event.target.closest("[data-like]");
    if (star) {
      var id = parseInt(star.dataset.like, 10);
      var list = likes();
      var index = list.indexOf(id);
      if (index === -1) { list.unshift(id); } else { list.splice(index, 1); }
      write(LIKES_KEY, list);
      renderAll();
      return;
    }
    var reset = event.target.closest("[data-reset]");
    if (reset) {
      try {
        localStorage.removeItem(LIKES_KEY);
        localStorage.removeItem(RECENT_KEY);
      } catch (error) { /* storage blocked */ }
      renderAll();
      var status = document.querySelector("[data-reset-status]");
      if (status) status.hidden = false;
    }
  });

  renderAll();
})();
