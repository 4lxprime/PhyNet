<?php

include 'utils.php';
include 'db/db_conn.php';

setHeaders();

$urlkey = htmlspecialchars($_GET['urlkey']);
$rip = htmlspecialchars($_GET['rip']);

?>

<?php

if (!isKey($urlkey)) {
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
    exit(401);
}

$stmt = $conn->prepare("SELECT gkey FROM gkeys WHERE relay=?");
$stmt->bind_param("s", $rip);
$stmt->execute();
$result = $stmt->get_result();

if (mysqli_num_rows($result) == 0) {
    echo json_encode("error", JSON_PRETTY_PRINT);
    exit(500);
}

$rows = $result->fetch_assoc();

echo json_encode($rows['gkey'], JSON_PRETTY_PRINT);
exit(200);

$stmt->close();

?>