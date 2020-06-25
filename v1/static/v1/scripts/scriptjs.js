
var rangeSlider = document.getElementById("rs-range-line");
var rangeBullet = document.getElementById("rs-bullet");
var rangeSliderbis = document.getElementById("rs-range-linebis");
var rangeBulletbis = document.getElementById("rs-bulletbis");

rangeSlider.addEventListener("input", showSliderValue, true);

rangeSliderbis.addEventListener("input", showSliderValuebis, true);


//setting the distance cursor
function showSliderValue() {
  rangeBullet.innerHTML = rangeSlider.value;
  var bulletPosition = (rangeSlider.value /rangeSlider.max);
  rangeBullet.style.left = (bulletPosition * 582) + "px";
}

//setting the price cursor
function showSliderValuebis() {
  rangeBulletbis.innerHTML = rangeSliderbis.value;
  var bulletPosition = (rangeSliderbis.value /rangeSliderbis.max);
  rangeBulletbis.style.left = (bulletPosition * 582) + "px";
}

function f(pos) {
  console.log(pos.coords.latitude + " "+ pos.coords.longitude)
}


if(navigator.geolocation){
  console.log("wesh la zone")
  navigator.geolocation.getCurrentPosition(f);
}
