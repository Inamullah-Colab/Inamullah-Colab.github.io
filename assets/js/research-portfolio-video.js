/* Muted playback respects reduced-motion preferences; native controls remain available. */
(function () {
  "use strict";
  var video = document.getElementById("research-portfolio-video");
  if (!video) return;

  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!motion.matches) {
    video.muted = true;
    video.autoplay = true;
    var playback = video.play();
    if (playback && typeof playback.catch === "function") {
      playback.catch(function () {
        // Native Play remains available when a browser declines autoplay.
      });
    }
  }

  motion.addEventListener("change", function (event) {
    if (event.matches) {
      video.autoplay = false;
      video.pause();
    }
  });
}());

