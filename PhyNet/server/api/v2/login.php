<?php

include 'utils.php';
include 'db/db_conn.php';

setHeaders();

$urlkey = htmlspecialchars($_GET['urlkey']);
$pass = htmlspecialchars($_GET['pass']);
$usr = htmlspecialchars($_GET['usr']);

// as we should get the sha256 version of the password
// this is now the final password version
$pass = hash('sha512', $pass);

?>

<?php

if (!isKey($urlkey)) {
    echo json_encode("bad_key", JSON_PRETTY_PRINT);
    exit(401);
}

$stmt = $conn->prepare("SELECT username FROM users WHERE username=? AND password=?");
$stmt->bind_param("ss", $usr, $pass);
$stmt->execute();
$result = $stmt->get_result();

if (mysqli_num_rows($result) == 0) {
    echo json_encode("nope", JSON_PRETTY_PRINT);
    exit(400);
}

echo json_encode("ok", JSON_PRETTY_PRINT);
exit(200);

$stmt->close();

?>

<?php

// not used, this function work and should be used each time
// we want to create a new user
function createAccount(string $usr, string $password): void {
    global $conn;

    $password = hash('sha256', $password);
    $password = hash('sha512', $password);

    $stmt = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    $stmt->bind_param("ss", $usr, $password);
    $result = $stmt->execute();

    if ($result) {
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        echo json_encode("error", JSON_PRETTY_PRINT);
    }
}

?>