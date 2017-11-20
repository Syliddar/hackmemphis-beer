<?php
    require __DIR__ . '/config.php';
    error_reporting(E_ERROR);
        if (!empty($_POST))
        {
            try {
                $link = new PDO("mysql:host=$dbhost;dbname=$dbname", $dbusername, $dbpassword);
                            $statement = $link->prepare("INSERT INTO Beer(time,sg, temp, beer_name, batch_id)VALUES(:time, :sg, :temp, :beer_name, :batch_id)");
                $response = $statement->execute(array(
                    "time" => htmlspecialchars($_POST["time"]),
                    "sg" => htmlspecialchars($_POST["sg"]),
                    "temp" => htmlspecialchars($_POST["temp"]),
                    "beer_name" => htmlspecialchars($_POST["beer_name"]),
                    "batch_id" => htmlspecialchars($_POST["batch_id"])
                ));
                echo 'Success. Inserted 1 row(s).';
            } catch (Exception $e) {
                echo 'Caught exception: ',  $e->getMessage();
            }
        }
        else
        {
            $link = new PDO("mysql:host=$dbhost;dbname=$dbname", $dbusername, $dbpassword);
            $statement = $link->prepare("SELECT entry_id, time, sg, temp, beer_name, batch_id FROM Beer order by time desc");
            $statement ->execute();
            $row = $statement->fetchAll(PDO::FETCH_ASSOC);
            echo json_encode($row);
        }
?>



