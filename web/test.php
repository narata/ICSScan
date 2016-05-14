<?php
    require_once('common.php');

    $query = "SELECT * FROM PortScans";
    $result = mysql_query($query);
    while($row = mysql_fetch_row($result))
    {
        foreach ($row as $key => $value) {
            echo $key ,':', $value;
        }
    }
?>

