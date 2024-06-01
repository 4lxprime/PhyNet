<?php

include 'utils.php';
include 'db/db_conn.php';

setHeaders();

$urlkey = htmlspecialchars($_GET['urlkey']);
$key = "VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";

?>

<?php

if (!isKey($urlkey)) {
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
    exit(401);
}

$stmt = $conn->prepare("SELECT MIN(relay_bots) FROM relays");
$stmt->execute();
$result = $stmt->get_result();

if (mysqli_num_rows($result) == 0) {
    echo json_encode("error", JSON_PRETTY_PRINT);
    exit(500);
}

$rbots = $result->fetch_assoc()['MIN(relay_bots)'];

$stmt = $conn->prepare("SELECT relay_ip FROM relays WHERE relay_bots=?");
$stmt->bind_param("s", $rbots);
$stmt->execute();

$resultSelect = $stmt->get_result();
$rows = $resultSelect->fetch_assoc();

$relay_ip = $rows['relay_ip'];

echo json_encode($relay_ip, JSON_PRETTY_PRINT);
exit(200);

$stmt->close();

?>