<?php
// Pengaturan koneksi database
$servername = "localhost";
$username = "root"; // Ubah sesuai dengan username database Anda
$password = ""; // Ubah sesuai dengan password database Anda
$dbname = "mqtt_database"; // Nama database

// Membuat koneksi ke database
$conn = new mysqli($servername, $username, $password, $dbname);

// Periksa koneksi
if ($conn->connect_error) {
    die("Koneksi ke database gagal: " . $conn->connect_error);
}

// URL API Python Flask
$api_url = "http://localhost:5000/mqtt_data";

// Mengambil data dari API JSON
$response = file_get_contents($api_url);
$data = json_decode($response, true);

// Menyimpan data ke dalam database
if ($data) {
    $timestamp = date("Y-m-d H:i:s"); // Waktu saat data diterima
    $temperature = $data['temperature'] ?? null;
    $humidity = $data['humidity'] ?? null;

    // Query untuk menyimpan data ke dalam tabel "mqtt_data_history"
    $sql = "INSERT INTO mqtt_data_history (timestamp, temperature, humidity) VALUES ('$timestamp', '$temperature', '$humidity')";

    if ($conn->query($sql) === TRUE) {
        echo "<p>Data berhasil disimpan ke database.</p>";
    } else {
        echo "<p>Error menyimpan data: " . $conn->error . "</p>";
    }

    // Menampilkan data dalam bentuk tabel
    echo "<h1>Data MQTT Terbaru</h1>";
    echo "<table border='1'>";
    echo "<tr><th>Timestamp</th><th>Temperature</th><th>Humidity</th></tr>";
    echo "<tr><td>$timestamp</td><td>$temperature</td><td>$humidity</td></tr>";
    echo "</table>";

    // Menampilkan histori data
    $result = $conn->query("SELECT * FROM mqtt_data_history ORDER BY timestamp DESC");
    if ($result->num_rows > 0) {
        echo "<h2>Histori Data</h2>";
        echo "<table border='1'>";
        echo "<tr><th>Timestamp</th><th>Temperature</th><th>Humidity</th></tr>";
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>{$row['timestamp']}</td><td>{$row['temperature']}</td><td>{$row['humidity']}</td></tr>";
        }
        echo "</table>";
    } else {
        echo "<p>Tidak ada histori data tersedia.</p>";
    }
} else {
    echo "<p>No data available</p>";
}

// Menutup koneksi
$conn->close();
?>

<!-- Meta tag untuk auto reload setiap 5 detik -->
<meta http-equiv="refresh" content="5">
