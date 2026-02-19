<h1>Sistema bancario <br>
(Descripcion de estructura sugerida cumpliendo los principios SOLID)</h1>


<strong>Carpeta Models</strong>
<p>Solo las clases.
<br><strong>Nota: </strong>Aqui no debe de haber logica de lectura de archivos</p>


<strong>Carpeta Services</strong>
<p>Aqui es pura logica de negocios</p>
<strong>Por ejemplo: </strong>
<ul>
  <li>Validar saldo antes de retirar</li>
  <li>Verificar si cuenta esta activa</li>
  <li>Ejecutar transferencias</li>
  <li>Generar reportes</li>
</ul>

<strong>Carpeta Repositories</strong>
<p>Responsables de</p>
<ul>
  <li>Leer y escribir en la base de datos (txt o csv)</li>
  <li>Convertir filas en objetos</li>
</ul>

<strong>Carpeta Analytics</strong>
<p>Aqui va todo lo relacionado a: </p>
<ul>
<li>Numpy</li>
<li>Anomalias</li>
<li>Graficos</li>
<li>NetworkX</li>

<strong>Carpeta Utils</strong>
<p>Aqui Funciones auxiliares: </p>
<ul>
<li>Validaciones</li>
<li>Manejo de fechas</li>
</ul>

<strong>Carpeta Data</strong>
<p>Base de datos simulada ya sea con CSV o TXT </p>






  
</ul>

