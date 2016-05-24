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
$website = $arguments['global']['site'];
$threads = $arguments['global']['threads'];
$timeout = $arguments['global']['timeout'];
$mode = $arguments['global']['mode'];
$choose_site = $arguments['global']['choose_site'];
$choose_poc = $arguments['global']['choose_poc'];
if($choose_poc == "poc")
	$choose_poc = $arguments['global']['poc_name'];
$command = "python ../vulscan/vulscan.py $website $mode $choose_site $choose_poc $threads $timeout";
exec($command, $out, $status);
if($status == 1)
    echo 4;
else echo $out[0];
?>