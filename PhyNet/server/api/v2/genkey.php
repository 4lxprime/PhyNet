<?php

include 'utils.php';
include 'db/db_conn.php';

setHeaders();

$urlkey = htmlspecialchars($_GET['urlkey']);
$gkey = htmlspecialchars($_GET['gkey']);
$ip = $_SERVER['REMOTE_ADDR'];

?>

<?php

if (!isKey($urlkey)) {
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
    exit(401);
}

$stmt = $conn->prepare("SELECT gkey FROM gkeys WHERE relay=?");
$stmt->bind_param("s", $ip);
$stmt->execute();
$result = $stmt->get_result();

if (mysqli_num_rows($result) == 0) {
    $stmt = $conn->prepare("INSERT INTO gkeys (gkey, relay) VALUES (?, ?)");
    $stmt->bind_param("ss", $gkey, $ip);
    $resultInsert = $stmt->execute();

    if (!$resultInsert) {
        echo json_encode("error", JSON_PRETTY_PRINT);
        exit(500);   
    }

} else {
    $row = $result->fetch_assoc();
    
    if ($rows['gkey'] != $gkey) {
        $stmt = $conn->prepare("UPDATE gkeys SET gkey=? WHERE relay=?");
        $stmt->bind_param("ss", $gkey, $ip);
        $resultUpdate = $stmt->execute();

        if (!$resultUpdate) {
            echo json_encode("error", JSON_PRETTY_PRINT);
            exit(500);   
        }    
    }
}

echo json_encode("ok", JSON_PRETTY_PRINT);
exit(200);

$stmt->close();

?>