<?php
$con = mysql_connect("localhost","sanamshakya","starfish");

if (!$con) {
  die('Could not connect: ' . mysql_error());
}

mysql_select_db("test_data", $con);

$sql = mysql_query("SELECT * FROM erts_lab_data");

while($r= mysql_fetch_array($sql)) {
    $datetime = $r['timestamp'];
    $result['category'][] = strtotime($datetime)*1000;
    $result['data'][] = round($r['humidity'],2) ;
	$result['data2'][] = round($r['temperature'],2);
}
print json_encode($result,  JSON_NUMERIC_CHECK);
mysql_close($con);
?> 