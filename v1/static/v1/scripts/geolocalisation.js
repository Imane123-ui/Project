function getPos(position) {
    let pos = position.coords
    document.getElementById("latitudeField").setAttribute("value", pos.latitude.toString())
    document.getElementById("longitudeField").setAttribute("value", pos.longitude.toString())
}

//getting the position when the page is loaded
navigator.geolocation.getCurrentPosition(getPos)

//updating the position every seconds
window.setInterval(function () {
    navigator.geolocation.getCurrentPosition(getPos)
}, 1000);
