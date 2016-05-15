<?php
require_once('common.php');
?>
<?php
//	check login first
if (!already_login()) {
	die();
}
?>

<?php

$arguments = $_REQUEST['config'];
$host = $arguments['global']['ip'];
$threads = $arguments['global']['threads'];
$timeout = $arguments['global']['timeout'];
$choose = $arguments['global']['choose'];
if($choose == "modbus")
	$command = "python ../protocol/modbus.py $host $threads $timeout";
system($command, $return_var);
echo $return_var[0];

?>