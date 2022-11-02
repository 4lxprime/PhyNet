<?php

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$urlkey=htmlspecialchars($_GET['urlkey']);
$pass=htmlspecialchars($_GET['pass']);
$usr=htmlspecialchars($_GET['usr']);
$pass=hash('sha512', $pass);
$key="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";

?>

<?php

include 'db/db_conn.php';

if ($urlkey===$key) {
    $sql="SELECT username FROM users WHERE username='$usr' AND password='$pass'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {

        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {

        echo json_encode("nope", JSON_PRETTY_PRINT);

    }

} else {

    echo json_encode("bad_key", JSON_PRETTY_PRINT);

}

function create_acc($usr, $pass) {

    global $conn;

    $pass=hash('sha256', $pass);
    $pass=hash('sha512', $pass);
    
    $sql="INSERT INTO users (username, password) VALUES ('$usr', '$pass')";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {

        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {

        echo json_encode("error", JSON_PRETTY_PRINT);

    }

}

?>