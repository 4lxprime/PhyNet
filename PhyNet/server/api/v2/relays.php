<?php

include 'utils.php';
include 'db/db_conn.php';

setHeaders();

$urlkey = htmlspecialchars($_GET['urlkey']);
$ip = htmlspecialchars($_GET['ip']);
$bots = htmlspecialchars($_GET['bots']);
$act = htmlspecialchars($_GET['act']);

?>

<?php

if (!isKey($urlkey)) {
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
    exit(401);
}

if ($act === "True") {
    $stmt = $conn->prepare("DELETE FROM relays");
    $stmt->execute();
    $result = $stmt->get_result();

    if (!$result) {
        echo json_encode("error", JSON_PRETTY_PRINT);
        exit(500);
    }

} else if ($act==="False") {
    $stmt = $conn->prepare("SELECT relay_ip, relay_bots FROM relays WHERE relay_ip=?");
    $stmt->bind_param("s", $ip);
    $stmt->execute();
    $result = $stmt->get_result();

    if (mysqli_num_rows($result) == 0) {
        $stmt = $conn->prepare("INSERT INTO relays (relay_ip, relay_bots) VALUES (?, ?)");
        $stmt->bind_param("ss", $ip, $bots);
        $resultInsert = $stmt->execute();

        if (!$resultInsert) {
            echo json_encode("error", JSON_PRETTY_PRINT);
            exit(500);
        }
        
    } else {
        $rows = $result->fetch_assoc();
        
        if ($rows['relay_bots'] != $bots) {
            $stmt = $conn->prepare("UPDATE relays SET relay_bots=? WHERE relay_ip=?");
            $stmt->bind_param("ss", $bots, $ip);
            $resultUpdate = $stmt->execute();
    
            if (!$resultUpdate) {
                echo json_encode("error", JSON_PRETTY_PRINT);
                exit(500);
            }
        }
    }
}

echo json_encode("ok", JSON_PRETTY_PRINT);
exit(200);

$stmt->close();

?>