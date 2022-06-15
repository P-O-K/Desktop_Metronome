
from 	timeit		import 	default_timer
from 	winsound	import 	Beep
from	threading	import 	Thread

import 	PySimpleGUI as 		GUI
import 	GlobalVars	as 		GO


def toggleAudioState( ) -> None:
	GO.PLAY_AUDIO = not GO.PLAY_AUDIO;
	return;


def beepTimer( ) -> None:
	ELAPSED_TIME = lambda S_TIME: default_timer( ) -S_TIME;
	while( not GO.STOP_THREAD ):
		
		S_TIME = default_timer( );
		while( ELAPSED_TIME( S_TIME ) < ( 60/GO.CURRENT_BPM )*.9 ): 	# *.9 for delay
			continue;

		if( GO.PLAY_AUDIO ):
			Beep( 440, 100 );
	return;



def clamp( BPM:int ) -> int:
	try: BPM = int( BPM );
	except: return GO.MIN_BPM;
	if int( BPM ) < GO.MIN_BPM: return GO.MIN_BPM;
	if int( BPM ) > GO.MAX_BPM: return GO.MAX_BPM;
	return int( BPM );



def toggleObjectText( WND:GUI.Window, ID:str, ALTER:list ) -> None:
	WND[ ID ].update( ALTER[0] if GO.PLAY_AUDIO else ALTER[1] );
	return;



def executeProgram( WND:GUI.Window ):
	while True:
		event, values = WND.read( );

		if( event in ( GUI.WIN_CLOSED, '_EXT_' ) ):
			GO.STOP_THREAD = True;
			break;

		if( event == '_SEL_' ):
			GO.CURRENT_BPM = clamp( values[ '_SEL_' ] );
			WND[ '_UIN_' ].update( GO.CURRENT_BPM );

		if( event == '_UIN_' ):
			GO.CURRENT_BPM = clamp( values[ '_UIN_' ] );
			WND[ '_SEL_' ].update( GO.CURRENT_BPM );

		if( event == '_RTS_' ):
			toggleObjectText( WND, '_RTS_', ['START', 'STOP'] );
			toggleAudioState( );

	return;



def initializeWindow( ) -> GUI.Window:
	LAYOUT = [  [ GUI.Input( GO.MIN_BPM, key='_UIN_', size=(3, 1), enable_events=True ), GUI.T( f'( {GO.MIN_BPM}-{GO.MAX_BPM} )' ) ],
				[ GUI.Slider( ( GO.MIN_BPM, GO.MAX_BPM ), key='_SEL_', orientation='h', disable_number_display=True, enable_events=True ) ],
				[ GUI.Button( 'START', key='_RTS_' ), GUI.Button( 'EXIT', key='_EXT_' ) ]  ];

	return GUI.Window( 'METRONOME' ).Layout( LAYOUT );



def openThreadLink( ) -> None:
	return Thread( target=beepTimer );



if __name__ == '__main__':
	TRD = openThreadLink( ).start( );
	WND = initializeWindow( );

	executeProgram( WND );
	
	WND.close( ); del TRD;
	raise SystemExit;