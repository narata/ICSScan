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

$command = "python ../portscan/scan.py $host $threads $timeout $choose";
system($command, $return_var);
echo $return_var[0];

?>