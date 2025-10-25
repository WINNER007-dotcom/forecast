navigator.geolocation.getCurrentPosition(
  (position) => {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    fetch(`/get_data?lat=${lat}&lon=${lon}`)
      .then((res) => res.json())
      .then((data) => {
        const box = document.getElementById("data");
        box.innerText = `City: ${data.city}
Temperature: ${data.temp}°C
Humidity: ${data.humidity}%
Condition: ${data.condition}
AQI: ${data.aqi} (${data.aqi_desc})`;

        // Show map
        const iframe = document.createElement("iframe");
        iframe.src = `https://www.google.com/maps?q=${lat},${lon}&hl=en&z=14&output=embed`;
        iframe.width = "100%";
        iframe.height = "100%";
        iframe.style.border = 0;
        document.getElementById("location").appendChild(iframe);
      })
      .catch((err) => {
        alert("Error fetching data!");
        console.error(err);
      });
  },
  (error) => {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        alert("Location permission denied!");
        break;
      case error.POSITION_UNAVAILABLE:
        alert("Location unavailable!");
        break;
      case error.TIMEOUT:
        alert("Location request timed out!");
        break;
      default:
        alert("An unknown error occurred!");
    }
  }
);
