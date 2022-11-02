<?php

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

$urlkey=htmlspecialchars($_GET['urlkey']);
$ip=htmlspecialchars($_GET['ip']);
$bots=htmlspecialchars($_GET['bots']);
$act=htmlspecialchars($_GET['act']);
$key="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0";

?>

<?php

include 'db/db_conn.php';

if ($urlkey===$key) {

    if ($act==="True") {
        $sql="DELETE FROM relays";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {

            echo json_encode("ok", JSON_PRETTY_PRINT);

        } else {

            echo json_encode("error", JSON_PRETTY_PRINT);

        }

    } else if ($act==="False") {
        $sql="SELECT relay_ip, relay_bots FROM relays WHERE relay_ip='$ip'";
        $result=mysqli_query($conn, $sql);

        if (mysqli_num_rows($result)==0) {
            $sql="INSERT INTO relays (relay_ip, relay_bots) VALUES ('$ip', '$bots')";
            $result=mysqli_query($conn, $sql);

            if ($result==TRUE) {
                
                echo json_encode("ok", JSON_PRETTY_PRINT);

            } else {

                echo json_encode("error", JSON_PRETTY_PRINT);

            }

        } else {
            $row=mysqli_fetch_assoc($result);
            
            if ($row['relay_bots']!=$bots) {
                $sql="UPDATE relays SET relay_bots='$bots' WHERE relay_ip='$ip'";
                $result=mysqli_query($conn, $sql);

                if ($result==TRUE) {

                    echo json_encode("ok", JSON_PRETTY_PRINT);

                } else {

                    echo json_encode("error", JSON_PRETTY_PRINT);

                }

            } else {
                
                echo json_encode("ok", JSON_PRETTY_PRINT);

            }

        }

    }

} else {

    echo json_encode("bad_key", JSON_PRETTY_PRINT);

}

?>