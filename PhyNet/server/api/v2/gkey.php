<?php

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$urlkey=htmlspecialchars($_GET['urlkey']);
$key="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";
$rip=htmlspecialchars($_GET['rip']);

?>

<?php

include 'db/db_conn.php';

if ($urlkey===$key) {

    $sql="SELECT gkey FROM gkeys WHERE relay='$rip'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
        $row=mysqli_fetch_assoc($result);

        echo json_encode($row['gkey'], JSON_PRETTY_PRINT);

    } else {

        echo json_encode("error", JSON_PRETTY_PRINT);

    }

} else {

    echo json_encode("bad_key", JSON_PRETTY_PRINT);

}

?>