<?php
require_once('common.php');

//
function search_scan($keyword='',$scanid=0){
	// $pKeyword = check_sql($keyword);
	$pKeyword = $keyword;
	$pId = $scanid;
	if ($userid = get_userid()) {
		// echo $userid . '<br>';
	}
	else{
		die();
	}
	// echo $userid . '<br>';
	// print $pLevel.$pKeyword;
	$query = "SELECT ID,Url,poc_name,poc_id,status,time FROM Scan WHERE ID > 0";
	if ($pKeyword !='') {
		$query .= " AND Url LIKE '%$pKeyword%'";
	}
	if (is_int($pId) and $pId>0) {
		$query .= " AND ID=$pId";
	}

	// echo $query.'<br>';

	$ret = array('data' => array(), );
	$result = mysql_query($query);
	while ($row = mysql_fetch_row($result)){
		// var_dump($row);
		foreach ($row as $key => $value){
			// echo $key.' => '.$value;
			$row[$key] = check_xss($value);
		}
		$ret['data'][] = $row;
		// var_dump($row);
	}
	return $ret;
}
?>
<?php
//	check login first
if (!already_login()) {
	die();
}

$keyword = check_sql(trim($_REQUEST['keyword']));
$scanID = (int)($_REQUEST['scanid']);
$data=search_scan($keyword,$scanID);
echo json_encode($data);
?>