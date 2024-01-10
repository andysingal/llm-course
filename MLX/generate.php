<?php
if ( ! file_exists( 'instructions.json' ) ) {
	die( 'Please provide an instructions.json file to get started.' );
}

function query_ollama( $prompt, $model = 'mistral', $context = '' ) {
	$ch = curl_init( 'http://localhost:11434/api/generate' );

	curl_setopt( $ch, CURLOPT_POSTFIELDS, json_encode([
		"model" => $model,
		"stream" => false,
		"prompt" => $context . $prompt
	] ) );
	curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );

	$response = curl_exec( $ch );

	if ( $response === false ) {
		die( 'API call failed: ' . curl_error($ch) );
	}

	$answer = json_decode( $response )->response;

	curl_close( $ch );

	return trim( $answer );
}

function create_valid_file() {
	if ( ! file_exists( 'train.jsonl' ) ) {
		die( 'No train.jsonl file found!' );
	}

	// Remove 20% of the training data and put it into a validation file
	$train = file_get_contents( 'train.jsonl' );
	$trainLines = explode( "\n", $train );
	$totalLines = count( $trainLines );
	$twentyPercent = round( $totalLines * 0.2 );

	$valLines = array_slice( $trainLines, 0, $twentyPercent );
	$trainLines = array_slice( $trainLines, $twentyPercent );

	$train = implode( "\n", $trainLines) ;
	$val = implode( "\n", $valLines );

	file_put_contents( 'train.jsonl', $train);
	file_put_contents( 'valid.jsonl', $val);
}

$json = file_get_contents( 'instructions.json' );
$instructions = json_decode( $json, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES );
$total = count( $instructions );

echo "------------------------------\n";
foreach ( $instructions as $i => $instruction ) {
	echo "(" . $i + 1 . "/" . $total . ") " . $instruction . "\n";
	echo "------------------------------\n";

	$answer = query_ollama( $instruction );
	echo $answer; // for terminal output

	$result = [ 'text' => '<s>[INST] ' . $instruction . '[/INST] ' . $answer . '</s>' ];

	$output = json_encode( $result ) . "\n";
	$output = str_replace( '[\/INST]', "[/INST]", $output );
	$output = str_replace( '<\/s>', "</s>", $output );

	echo "\n\n------------------------------\n";

	file_put_contents( 'train.jsonl', $output, FILE_APPEND );
}

create_valid_file();

echo "Done! Training and validation JSONL files created.\n";
