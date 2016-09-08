<?php
// Eerst creeer ik random potentiele oplossingen in een multidimensionale array. Ze hoeven dus niet per se te kloppen. Lastig hierbij
// is dat je moet voorkomen dat twee Queens op dezelfde plek komen en dat er in totaal dus echt 8 queens zijn.

for($k = 0; $k < 5; $k++){
        $totalitems = 0;
        while($totalitems < 8){        
                $rand1 = rand(0, 7);
                $rand2 = rand(0, 7);            
                $aBoard[$rand1][$rand2] = 'Q';
        
                for($i = 0; $i < 8; $i++){
                        $nia[$i] = count($aBoard[$i]);
                }
                $totalitems = $nia[0] + $nia[1] + $nia[2] + $nia[3] + $nia[4] + $nia[5] + $nia[6] + $nia[7];  
        }
        $aSolutions[$k] = $aBoard;
}

        
        
// Ff laten zien in een tabel

for($h = 0; $h < 5; $h++){
        echo "<table border='1px solid black'>";
                for($i = 0; $i < 8; $i++){
                        echo "<tr>";
                                for($j = 0; $j < 8; $j++){
                                        echo "<td height='25px' width='25px'>" . $aSolutions[$h][$i][$j] . "</td>";
                                }
                        echo "</tr>";
                }
        echo "</table>" . "<br>";
}


?>
