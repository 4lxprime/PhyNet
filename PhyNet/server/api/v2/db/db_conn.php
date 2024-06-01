<?php
$sname = "localhost";
$unmae = "root";
$password = "";
$db_name = "phybot";
$conn = mysqli_connect($sname, $unmae, $password, $db_name);

if (!$conn) {
	echo json_encode("db_connection_failed", JSON_PRETTY_PRINT);
}
?>