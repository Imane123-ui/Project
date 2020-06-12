
var rangeSlider = document.getElementById("rs-range-line");
var rangeBullet = document.getElementById("rs-bullet");
var rangeSliderbis = document.getElementById("rs-range-linebis");
var rangeBulletbis = document.getElementById("rs-bulletbis");

rangeSlider.addEventListener("input", showSliderValue, true);

rangeSliderbis.addEventListener("input", showSliderValuebis, true);

function showSliderValue() {
  rangeBullet.innerHTML = rangeSlider.value;
  var bulletPosition = (rangeSlider.value /rangeSlider.max);
  rangeBullet.style.left = (bulletPosition * 582) + "px";
}

function showSliderValuebis() {
  rangeBulletbis.innerHTML = rangeSliderbis.value;
  var bulletPosition = (rangeSliderbis.value /rangeSliderbis.max);
  rangeBulletbis.style.left = (bulletPosition * 582) + "px";
}
