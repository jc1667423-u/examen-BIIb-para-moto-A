import re, random, json

with open('contenido_pdf.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Clean up
raw = re.sub(r'=== PAGINA \d+ ===', '', raw)
raw = raw.replace('\r\n', '\n').replace('\r', '\n')

# Manually defined questions from the PDF (question -> correct answer)
# Extracted by reading the PDF content carefully
qa_pairs = [
    ("Respecto de los dispositivos de control o regulación del tránsito:", "Los conductores y los peatones están obligados a su obediencia, salvo instrucción de la Policía Nacional del Perú asignada al tránsito que indique lo contrario."),
    ('La señal vertical reglamentaria R-6 "prohibido voltear a la izquierda", significa que:', "Está prohibido voltear a la izquierda y, por lo tanto, también está prohibido el giro en U."),
    ("La señal vertical reglamentaria R-3 significa que:", "El único sentido de desplazamiento es continuar de frente."),
    ("En las vías, las marcas en el pavimento que son del tipo central discontinua y de color amarillo significan que:", "Está permitido cruzar al otro carril para el adelantamiento vehicular, si es que es seguro hacerlo."),
    ("El color ámbar o amarillo del semáforo significa que:", "Los vehículos deben detenerse antes de ingresar a la intersección si su velocidad y ubicación lo permiten; de lo contrario, deberán cruzar y despejar la intersección."),
    ("Los colores del semáforo tienen el siguiente significado: rojo:____; ámbar o amarillo:_____; verde:________.", "Detención - prevención - paso."),
    ("¿Qué indica una flecha verde en un semáforo vehicular?", "Se puede continuar con precaución únicamente en la dirección de la flecha y desde el carril que esta flecha controla."),
    ("La siguiente señal vertical reglamentaria R-53:", "Prohíbe al conductor detener el vehículo dentro del área de la intersección."),
    ("Si llega a una intersección y visualiza el semáforo con una flecha roja hacia la izquierda y la luz circular verde prendidas al mismo tiempo, la acción correcta es:", "Avanzar, pero el giro a la izquierda está prohibido por la flecha roja."),
    ("Si llega a una intersección donde el semáforo muestra una luz intermitente, qué afirmación es correcta:", "Si la luz intermitente es ámbar, tiene preferencia, debiendo reducir la velocidad y continuar con precaución."),
    ("¿La luz intermitente roja es igual que una señal de PARE?", "Verdad."),
    ("Al aproximarse a una intersección con giro permitido a la izquierda, la conducta correcta es:", "Hacer la señal de volteo a la izquierda con las luces direccionales, ubicar con antelación el vehículo en el carril de circulación de la izquierda y girar con precaución."),
    ("Al cambiar de carril en una vía de un solo sentido con múltiples carriles, ¿cuál es la conducta correcta?", "Se deben encender las luces direccionales primero, buscar una brecha y realizar el cambio de carril con precaución."),
    ("Respecto a los cruces a nivel con vías férreas, señale la afirmación correcta:", "Los vehículos que transitan por la vía férrea tienen preferencia de paso sobre los que transitan por la vía que la cruza."),
    ("Ante la señal de color rojo del semáforo y la indicación de continuar la marcha del efectivo de la Policía Nacional del Perú asignado al control del tránsito, corresponde:", "Continuar la marcha."),
    ("Está prohibido estacionar un vehículo:", "Todas las alternativas son correctas."),
    ("La siguiente señal vertical reglamentaria R-29:", "Prohíbe el uso de la bocina."),
    ("Se le impondrá el pago de una multa y no podrá obtener la licencia de conducir por 3 años a la persona que:", "Conduzca un vehículo automotor sin tener licencia de conducir."),
    ("En el supuesto que se encuentre manejando y un vehículo que tiene la intención de sobrepasarlo o adelantarlo lo alcance, ¿qué debería hacer usted?", "No debe aumentar la velocidad hasta que el vehículo lo sobrepase."),
    ("¿Cuál de las siguientes afirmaciones es correcta?", "El conductor debe respetar los límites máximos y mínimos de velocidad establecidos."),
    ("En la circulación vehicular, es correcto afirmar que:", "Los vehículos deben circular dentro de las líneas de carril, salvo cuando se realicen las maniobras que indica el Reglamento Nacional de Tránsito."),
    ("En caso de accidentes, el SOAT cubre los daños que sufren:", "Los ocupantes y terceros no ocupantes del vehículo."),
    ("¿Cuál de los siguientes seguros es exigible para conducir un vehículo automotor?", "El Seguro Obligatorio de Accidentes de Tránsito - SOAT."),
    ("Cuándo es obligatorio darle preferencia de paso a un vehículo de emergencia o vehículo oficial:", "Cuando emita señales audibles y visibles."),
    ("Si por el carril por donde está conduciendo se aproxima a un vehículo de transporte escolar que se encuentra detenido, recogiendo o dejando escolares ¿Qué debe hacer?", "Detener el vehículo y no continuar la marcha hasta que haya culminado el ascenso o descenso de los escolares."),
    ("¿Qué significa un triángulo rojo de seguridad colocado en la calzada?", "La presencia de un vehículo inmovilizado en la vía pública por alguna circunstancia."),
    ("¿En la conducción vehicular, existe excepción a la obligación de conservar la distancia obligatoria entre vehículos?", "Si existe, y es para los cortejos fúnebres, convoyes militares y policiales y caravanas autorizadas."),
    ("En intersecciones que no tienen señales de Pare, Ceda el Paso o Semáforo, ¿las vías de doble sentido tienen prioridad de paso respecto a las vías de un solo sentido de igual clasificación?", "Sí."),
    ("Si usted se aproxima a una señal de PARE colocada verticalmente o pintada en la vía, la acción correcta es:", "Parar por completo, ceder el paso a los usuarios que tengan preferencia y luego continuar con precaución."),
    ("¿Cuál es la diferencia entre las señales P-2A y P-1A?", "La señal P-1A advierte la presencia de curva pronunciada a la derecha mientras que la P-2A advierte la presencia de curva suave a la derecha."),
    ("¿Qué indica la señal R-30F?", "Regula la velocidad máxima permitida en curvas."),
    ("¿Que indica la siguiente señal R-23?", "Prohibida la circulación de motocicletas."),
    ("Si dos vehículos se aproximan simultáneamente a una intersección no regulada (sin señalización) procedentes de vías diferentes, ¿quién tiene preferencia de paso?", "El que se aproxime por la derecha del otro."),
    ("En una intersección no regulada (sin señalización) tiene preferencia de paso:", "El vehículo que ingresó primero a la intersección."),
    ("En una rotonda, tiene prioridad de paso el vehículo que:", "Circula por ella."),
    ("El sobrepaso o adelantamiento de un vehículo en movimiento se efectúa, salvo excepciones, por la ___ retornando el vehículo después de la maniobra a su carril original.", "Izquierda."),
    ("Si un conductor está tomando medicamentos y por ello siente sueño ¿qué debe hacer?", "Abstenerse de manejar."),
    ("Son documentos que deben portarse obligatoriamente, durante la conducción del vehículo, y exhibirse cuando la autoridad competente lo solicite:", "Documento de identidad, SOAT vigente (puede ser virtual) y tarjeta de identificación vehicular."),
    ("La siguiente señal indica:", "Que solo las motocicletas pueden circular por la vía o carril."),
    ("Al cambiar de dirección, un conductor debe:", "Señalizar toda la maniobra hasta su culminación."),
    ("¿Está permitido conducir un vehículo con el motor en punto neutro?", "No, está prohibido."),
    ("Si la licencia de conducir no se encuentra vigente, los vehículos que autoriza a conducir dicha licencia:", "No podrán ser conducidos."),
    ("De acuerdo con el sistema de control de licencias de conducir por puntos:", "Determinadas infracciones suman puntos."),
    ("¿Cuál es la consecuencia de acumular 100 puntos en la licencia de conducir en un período de 24 meses?", "Suspensión de licencia de conducir."),
    ("Se entiende por carril a la:", "Parte de la calzada destinada al tránsito de una fila de vehículos."),
    ("Se entiende por línea de parada a:", "La línea transversal marcada en la calzada antes de la intersección, que indica al conductor el límite para detener el vehículo."),
    ("La siguiente señal vertical reglamentaria P-17A, indica:", "Reducción de la calzada en ambos lados."),
    ("En caso de encontrar marcación de doble línea amarilla compuesta por un trazo continuo y otro trazo discontinuo en una vía de doble sentido, ¿qué se debe hacer?", "Respetar la línea que está de su lado (si es continua, no adelantar; si es discontinua, está permitido adelantar)."),
    ("Se define como zona rígida al:", "Área de la vía en la que se prohíbe el estacionamiento de vehículos."),
    ("La posición de frente o de espaldas ejecutada por el efectivo de la Policía Nacional del Perú asignado al control de tránsito significa:", "Obligación de detenerse de quien así lo enfrente."),
    ("Siempre que no exista una señal de límite de velocidad, en zonas urbanas el límite máximo de velocidad en calles y jirones es de:", "40 km/h."),
    ("Siempre que no exista una señal de límite de velocidad, en zonas urbanas el límite máximo de velocidad en avenidas es de:", "60 km/h."),
    ("Siempre que no exista una señal de límite de velocidad en zonas urbanas, el límite máximo de velocidad en zona escolar es de:", "30 km/h."),
    ("Siempre que no exista una señal de límite de velocidad en carreteras, el límite máximo de velocidad para automóviles, camionetas y motocicletas es de:", "100 km/h."),
    ("Siempre que no exista una señal de límite de velocidad en carreteras, el límite máximo de velocidad es de:", "100 km/h. para automóviles, camionetas y motocicletas."),
    ("Siempre que no exista una señal de límite de velocidad mínima, el límite mínimo de velocidad en zona urbana y en carreteras es de:", "La mitad de la velocidad máxima establecida para cada tipo de vía."),
    ("¿Cuál es la sanción por conducir con presencia de alcohol en la sangre en proporción mayor a lo previsto en el Código Penal, o bajo los efectos de estupefacientes, narcóticos y/o alucinógenos comprobado con el examen respectivo, o por negarse al mismo y que haya participado en un accidente de tránsito?", "Multa, cancelación de la licencia de conducir e inhabilitación definitiva para obtener una licencia de conducir."),
    ("¿Cuál es la sanción si en un operativo de alcoholemia usted es intervenido y se comprueba que ha consumido alcohol por encima del límite legal, o está conduciendo bajo los efectos de estupefacientes, narcóticos y/o alucinógenos comprobada con el examen respectivo?", "Multa y suspensión de la licencia de conducir por 3 años."),
    ("La frecuencia de la inspección técnica de una moto (categoría L3) y de un sidecar (categoría L4) es:", "Cada año."),
    ("¿Cuál es el plazo de vigencia del SOAT?", "1 año."),
    ("Si ocurre un accidente de tránsito, ¿qué obligación tiene el conductor, el propietario del vehículo o el prestador del servicio de transporte?", "Dar aviso a la compañía de seguros y dejar constancia en la delegación de la Policía Nacional del Perú más cercana."),
    ("Si una licencia de conducir consigna alguna restricción, es correcto afirmar que:", "Es una obligación cumplir con la restricción."),
    ("La señal preventiva P-33A, significa:", "Señal de proximidad de un reductor de velocidad tipo resalto."),
    ("¿Está permitido usar la bocina de su vehículo para advertir al conductor del vehículo que circula delante, que será adelantado?", "No, está prohibido."),
    ("Si observa que se aproxima una ambulancia sin las luces especiales encendidas y sin sirena, es correcto afirmar que:", "No estamos obligados a darle preferencia de paso."),
    ("Si se encuentra en una intersección y se enciende la luz verde del semáforo y observa que en la calle transversal hay vehículos o personas despejando la intersección, ¿qué debe hacer?", "No iniciar la marcha hasta que el vehículo o las personas terminen de cruzar."),
    ("En señalética vial, el color ____ en el pavimento es utilizado para carriles de tráfico en sentido opuesto y el color ____ en el pavimento es utilizado como separador de carriles de tráfico en el mismo sentido.", "Amarillo - blanco."),
    ("Si una fila de escolares cruza la calzada fuera del crucero peatonal, ¿qué acción se debe tomar?", "Parar y ceder el paso."),
    ("Si se aproxima a una zona escolar, ¿que acción debe realizar?", "Disminuir la velocidad a 30 Km/h."),
    ("Tienen el objetivo de notificar a los usuarios las limitaciones, prohibiciones o restricciones en el uso de la vía.", "Señales reguladoras o de reglamentación."),
    ("Tienen el propósito de advertir a los usuarios sobre la existencia y naturaleza de un peligro en la vía.", "Señales preventivas."),
    ("Es una infracción de tránsito:", "Todas las alternativas son correctas."),
    ("¿Qué debería hacer el conductor al acercarse a una señal de 'CEDA EL PASO' en una intersección?", "Disminuir la velocidad, parar si es necesario y ceder el paso a los peatones o vehículos que circulan por la vía transversal."),
    ("No se debe conducir un vehículo:", "Todas son correctas."),
    ("¿Qué debe hacer si se aproxima a una intersección sin semáforo y sin presencia de la Policía de Tránsito, y observa que un peatón está cruzando por el paso peatonal?", "Detener el vehículo y ceder el paso al peatón."),
    ("Sobre el uso del casco protector en la conducción de la motocicleta, es correcto afirmar que:", "El uso del casco es obligatorio para el conductor y el acompañante."),
    ("Las motocicletas al circular por una vía deben hacerlo por el carril de____", "La derecha."),
    ("Sobre el uso de la bocina del vehículo, es correcto afirmar que:", "El conductor únicamente debe utilizar la bocina para evitar situaciones peligrosas."),
    ("Una línea blanca continua en el sentido longitudinal de una vía, que se coloca en el pavimento, le indica al conductor:", "Que está prohibido pasar al otro lado de la línea con algunas excepciones."),
    ("¿Cuál es el número máximo de personas que puede transportar una motocicleta?", "Es igual al número de asientos señalados en la tarjeta de identificación vehicular."),
    ("La acción correcta al abastecer de combustible su vehículo, es:", "Abstenerse de fumar tanto el conductor como sus acompañantes."),
    ("Si usted desea realizar una competencia de carreras entre su vehículo y otro vehículo motorizado; para ello puede utilizar:", "Un circuito de carrera, autódromo o pista de aceleración autorizado por la autoridad competente."),
    ("Señale cuál de las siguientes conductas constituye una infracción al tránsito:", "Todas las alternativas son correctas."),
    ("La marcas en el pavimento constituyen un elemento indispensable para la operación vehicular, pues su función es:", "Reglamentar la circulación, así como advertir y guiar a los usuarios de la vía."),
    ("Las marcas en el pavimento de color ________complementan las señales informativas, como por ejemplo las zonas de estacionamiento para personas con movilidad reducida.", "Azul."),
    ("La línea central de color amarillo en el pavimento es continua cuando:", "No está permitido cruzar al otro carril."),
    ("Si un conductor que circula por el carril derecho de una vía se encuentra con las flechas inclinadas que se muestran en la figura, su conducta correcta es:", "Cambiarse al carril izquierdo con precaución."),
    ("Si durante la conducción vehicular, un efectivo de la Policía de Tránsito le solicita al conductor someterse a una prueba de alcoholemia; la acción correcta del conductor es:", "Someterse a la prueba de alcoholemia, ya que está obligado a ello ante la solicitud del efectivo de la Policía de Tránsito."),
    ("¿Cuál de las siguientes conductas no es una infracción de tránsito?", "Detenerse totalmente en una señal de PARE cuando no hay peatones y/o vehículos circulando por la vía transversal."),
    ("Si la persona conduciendo sale de su propiedad y tiene que cruzar la acera e ingresar a una vía, la conducta correcta es:", "Dar preferencia de paso a los vehículos que circulan por la vía y a los peatones que circulan por la acera."),
    ("¿Qué significa una línea continua blanca pintada entre el carril de la derecha y la berma de una carretera?", "Que no se debe conducir atravesándola, al menos que haya una situación de emergencia."),
    ("En el caso representado en el siguiente gráfico ¿el vehículo rojo puede rebasar al azul?", "No puede hacerlo."),
    ("La siguiente señal (R-17), significa:", "Prohibida la circulación de vehículos automotores."),
    ("Si usted se encuentra conduciendo su vehículo por una vía y antes de cruzar la intersección se encuentra con la señal R-4, esta le indica:", "Que está por ingresar a una vía de sentido contrario y no debe entrar."),
    ("La siguiente señal (P-36), significa:", "Superficie deslizante."),
    ("La siguiente señal (R-14), significa:", "Circular solo en el sentido indicado por la flecha."),
    ("La siguiente señal (P-6) significa:", "La proximidad de un cruce o intersección de 2 vías al mismo nivel en ángulo recto."),
    ("La siguiente señal (R-30C), significa:", "Que al salir de la vía por donde está circulando, la velocidad máxima es 50 km/h."),
    ("La siguiente señal (R-5-4), significa:", "Que la intersección contempla giros tangentes a la izquierda en ambos sentidos."),
    ("La siguiente señal (R-9), significa:", "Que está permitido el giro en U."),
    ("La siguiente señal (R-5-2), significa:", "Que el carril por donde circula permite girar a la izquierda o seguir de frente."),
    ("La siguiente señal (R-20), significa:", "Que los peatones deben circular por la izquierda."),
    ("Es una conducta que se sanciona:", "Todas las anteriores."),
    ("La siguiente señal (R-48), significa:", "Zona de carga y descarga."),
    ("La siguiente señal (R-49), significa:", "Se debe mantener la distancia de seguridad entre vehículos."),
    ("La siguiente señal (R-50), significa:", "Que si solo hay un carril no tiene preferencia el que está mirando la señal y debe darle paso al del sentido contrario."),
    ("La señal (R-5-1), es:", "Una señal de obligación."),
    ("La señal (P-3A), le indica al conductor que:", "Hay una curva y contra-curva pronunciada a la derecha."),
    ("La siguiente señal (P-5-1A), le advierte al conductor que:", "Se aproxima a un camino sinuoso a la izquierda."),
    ("La siguiente señal (P-61), le advierte al conductor que:", "Está circulando por una curva horizontal."),
    ("La siguiente señal (P-34), le advierte al conductor que:", "Se aproxima a un badén."),
    ("La siguiente señal (P-60), es:", "Una señal preventiva."),
    ("La siguiente señal (P-46), indica:", "Ciclistas en la vía."),
    ("La siguiente señal (P-46-A), indica:", "Que nos aproximamos a un cruce de ciclovía."),
    ("La siguiente señal (P-46B), indica:", "La ubicación de un cruce de ciclistas."),
    ("La siguiente señal (P-48), indica:", "Zona con presencia de peatones."),
    ("La siguiente señal (P-48A), indica:", "Proximidad a un cruce peatonal."),
    ("La siguiente señal (P-48-B), indica:", "Ubicación de un cruce peatonal."),
    ("La siguiente señal (P-49), indica:", "Zona escolar."),
    ("La siguiente señal (P-49A), indica:", "Proximidad a un cruce escolar."),
    ("La siguiente señal (P-49B), indica:", "Ubicación de un cruce escolar."),
    ("La siguiente señal (P-50), indica:", "Niños jugando."),
    ("La siguiente señal (P-51), indica:", "Maquinaria agrícola en la vía."),
    ("La siguiente señal (P-53), indica:", "Animales en la vía."),
    ("La siguiente señal (P-55), indica:", "Proximidad a un semáforo."),
    ("La siguiente señal (P-58), le indica:", "Que usted se aproxima a una señal de PARE."),
    ("La siguiente señal (P-59), le indica:", "Que usted se aproxima a una señal de CEDA EL PASO."),
    ("La siguiente señal (P-41), le indica:", "Que usted se aproxima a un túnel."),
    ("La siguiente señal (P-45), indica:", "Vuelo de aviones a baja altura."),
    ("La siguiente señal (P-52), le indica:", "Que se aproxima a una salida de vehículos de bomberos."),
    ("La siguiente señal (P-66), le indica:", "Que se aproxima una zona donde hay ráfagas de viento lateral."),
    ("La siguiente señal (P-66A), le indica:", "Que se acerca a una zona de arenamiento en la vía."),
    ("Si al conducir su vehículo se encuentra con la señal vertical que se muestra (prohibido girar izquierda con ruta alternativa), usted debe entender que:", "En la siguiente intersección está prohibido girar a la izquierda y por lo tanto, si desea seguir esa ruta debe tomar el camino alternativo que muestra la señal."),
    ("Si al conducir su vehículo se encuentra con la señal vertical que se muestra (giro izquierda vuelta manzana), usted debe entender que:", "Si quiere girar a la izquierda debe pasar la intersección y dar la vuelta a la manzana."),
    ("La siguiente señal (I-14), significa:", "Señal de hospital."),
    ("La siguiente señal (I-31), significa:", "Proximidad de un estacionamiento para emergencias."),
    ("La siguiente señal (I-9), significa:", "Zona militar."),
    ("La siguiente señal (I-18), se utiliza para indicar:", "Cercanía a un servicio mecánico."),
    ("La siguiente señal (I-19), se utiliza para indicar:", "Cercanía a un grifo."),
    ("La siguiente señal (I-20), se utiliza para indicar:", "Cercanía a una llantería."),
    ("La siguiente señal (R-16A), se utiliza para indicar:", "Fin de la restricción de prohibido adelantar."),
    ("El comportamiento del conductor como usuario de la vía, debe estar orientado a:", "Todas las alternativas son correctas."),
    ("Son considerados usuarios vulnerables de la vía y por tanto merecen especial protección:", "Peatones, niños, adultos mayores, personas con movilidad reducida, ciclistas."),
    ("La siguiente señal (P-61), muestra:", "Delineadores de curva, que guían al conductor."),
    ("El conductor está ____ a las pruebas que le solicite el Efectivo de la Policía Nacional del Perú, asignado al control del tránsito, para determinar su estado de intoxicación por alcohol, drogas, estupefacientes u otros tóxicos", "Obligado - someterse."),
    ("Ante un conductor con evidente discapacidad física, la cual no figura en el rubro de restricciones de su licencia de conducir, procede:", "Que la Policía de Tránsito intervenga a dicho conductor y que la autoridad que expidió la licencia de conducir ordene su reexaminación."),
    ("Es una obligación general de tránsito que, los ___________ circulen respetando los mensajes de ________, las instrucciones de los Efectivos de la Policía de Tránsito y el mandato de las normas legales y reglamentarias correspondientes.", "Los usuarios de la vía pública - los dispositivos de control de tránsito."),
    ("Marque la afirmación incorrecta:", "Las motocicletas pueden compartir un mismo carril con otro vehículo al circular."),
    ("¿Si al conducir por una avenida se encuentra con una señal en la vía que indica un límite máximo de 50 km/h, sin embargo, conforme a lo dispuesto en la norma el límite máximo de velocidad en dicha vía es de 60 km/h; usted:", "Debe obedecer la señal de velocidad instalada en la vía."),
    ("Indique la conducta permitida:", "El estacionamiento de un vehículo de emergencia en un lugar no permitido, si ello fuera imprescindible."),
    ("Se considera el abandono de un vehículo cuando:", "El vehículo está estacionado en un lugar permitido en la vía pública, pero sin conductor y por un tiempo mayor de 48 horas."),
    ("El servicio de taxi en motos lineales:", "No está permitido."),
    ("Sobre la emisión vehicular de sustancias contaminantes, marque la opción correcta:", "Está prohibida, en un índice superior al límite máximo que permite la norma."),
    ("La autoridad competente, puede prohibir o restringir ____ en determinadas vías públicas.", "Cuando la situación lo justifique - la circulación o estacionamiento de vehículos."),
    ("La detención de un vehículo debe efectuarse:", "En el sentido de la circulación y en el carril derecho de la vía."),
    ("En caso de un accidente de tránsito con daños personales y/o materiales los participantes deben:", "Solicitar la intervención de la autoridad policial."),
    ("La faculta y autoriza la circulación del vehículo por la vía pública, identifica el bien, y, por ende, al titular responsable de las acciones que deriven de su propiedad.", "Placa Única Nacional de Rodaje."),
    ("¿Después de qué tiempo de haber cometido la misma infracción se llama reincidencia y es sancionada con el doble de la multa establecida?", "12 meses."),
    ("Si a un conductor infractor le suspendieron su licencia de conducir, éste se encuentra facultado para:", "Ninguna de las alternativas es correcta."),
    ("Las ____ tienen por función informar a los usuarios sobre los servicios generales existentes próximos a la vía, tales como teléfono, hospedaje, restaurante, primeros auxilios, estación de combustibles, talleres, y otros.", "Señales de servicios generales."),
    ("¿Constituye una infracción tramitar el duplicado de una licencia de conducir que se encuentra retenida?", "Si, constituye una infracción."),
    ("Las marcas en el pavimento constituyen la señalización _____y se emplean para _________ la circulación.", "Horizontal - reglamentar."),
    ("Ciclista es a ciclovía como:", "Conductor - calzada."),
    ("La siguiente señal (P-15), se utiliza para advertir al conductor:", "La proximidad de una intersección rotatoria (óvalo o rotonda)."),
    ("La siguiente señal (P-31A), indica:", "La proximidad del final de la vía."),
    ("Es una línea transversal a la calzada, que indica al conductor que debe detener completamente el vehículo, no debiendo sobrepasar el inicio de la indicada línea:", "Línea de pare."),
    ("Los semáforos son:", "Dispositivos de control del tránsito que tienen por finalidad regular y controlar el tránsito vehicular, motorizado y no motorizado, y el peatonal, a través de las indicaciones de las luces respectivas."),
    ("La conducción requiere un alto nivel de atención, pues existen distracciones que pueden ocasionar accidentes de tránsito, como, por ejemplo:", "Todas las alternativas son correctas."),
    ("¿Influye la somnolencia en la capacidad de conducir?", "Si, pues el conductor tomará decisiones lentas que lo inducirán a cometer errores."),
    ("¿Cuál es la acción correcta del conductor, según las normas de tránsito, en la situación que plantea el siguiente gráfico?", "Dar preferencia de paso al peatón para que cruce la calzada."),
    ("¿En cuál de las siguientes opciones, los factores mencionados contribuyen a una colisión vehicular?", "Pavimento húmedo, neumáticos desgastados, cansancio."),
    ("La ____ es la parte de una carretera o camino contigua a la calzada, no habilitada para la circulación de vehículos y destinada eventualmente a la detención de vehículos en emergencia y circulación de peatones.", "Berma."),
    ("Es una parte de la vía destinada a la circulación de vehículos y eventualmente al cruce de peatones y animales.", "La calzada."),
    ("Es una parte de la vía destinada al uso de peatones", "La acera."),
    ("Son señales que regulan el tránsito:", "Las señales verticales y las marcas en la calzada o señales horizontales."),
    ("El conductor que en una vía urbana va a girar a la izquierda, a la derecha o en 'U' debe hacer la señal respectiva con la luz direccional, por lo menos:", "20 metros antes de realizar la maniobra."),
    ("Si usted está conduciendo por una carretera y va girar a la izquierda, debe realizar la señal respectiva con la luz direccional por lo menos:", "30 metros antes de realizar la maniobra."),
    ("¿La licencia de la Clase B, permite conducir autos?", "No."),
    ("El siguiente gráfico muestra:", "Señalización de tránsito vertical y horizontal en una zona escolar."),
    ("Las ____ canalizadoras, tiene por función conformar las islas canalizadoras del tránsito automotor en una ____.", "Líneas - intersección."),
    ("Si al conducir en una intersección se encuentra con las siguientes marcas en el pavimento (malla ortogonal de color amarillo), significa:", "Que no puede detener el vehículo dentro del área de intersección."),
    ("De acuerdo al siguiente gráfico, es correcto afirmar que:", "La zona de no adelantar inicia con las líneas amarillas continuas."),
    ("Cuál de las siguientes alternativas, no es una infracción de tránsito:", "Detenerse en luz verde, para ceder el paso a un peatón."),
    ("Existe infracción al tránsito cuya sanción sea nunca más obtener una licencia de conducir?", "Si existe, y una de ellas es por conducir con presencia de alcohol en mayor grado al permitido y participar en un accidente de tránsito."),
    ("Los ____ y las ____ requieren un carril completo para circular con seguridad.", "Todas las anteriores."),
    ("El conductor de un vehículo debe reducir la velocidad, siempre que se encuentre en los siguientes casos:", "En intersecciones, curvas, túneles, puentes."),
    ("El pasajero de una motocicleta debe saber:", "Todas las anteriores."),
    ("En la relación 'conductores de vehículos menores' (por ejemplo, una motocicleta) y 'conductores de vehículos mayores' (por ejemplo un auto sedan), la afirmación correcta es:", "Los conductores de vehículos menores tienen las obligaciones y derechos aplicables a los conductores de vehículos mayores, excepto aquellos que por su naturaleza no les son aplicables."),
    ("Antes de iniciar la conducción de una motocicleta, el conductor debe:", "Todas las alternativas son correctas."),
    ("El equipo de protección más importante al conducir una motocicleta, es:", "Casco."),
    ("La posición correcta del motociclista en la conducción es:", "Las alternativas b y c son correctas."),
    ("La siguiente afirmación: 'el motociclista que se encuentra conduciendo en un carril, no debe permitir que otros vehículos intenten forzarlo a moverse hacia un costado del mismo', es:", "Verdadera."),
    ("La agilidad de la moto _____debe ser __________ para ir en _______ entre vehículos:", "Nunca - aprovechada - zig zag."),
    ("La conducción eficiente, tiene como beneficio:", "Cuidado del medioambiente, ahorro de combustible o energía."),
    ("La siguiente señal de autorización, le indica que:", "Permite el giro a la izquierda en una intersección con semáforo en luz roja."),
    ("Es una técnica de conducción eficiente, y por tanto permite la reducción del consumo de combustible, así como de la contaminación ambiental:", "Las alternativas a y b son correctas."),
    ("La posición correcta de los pies al conducir una motocicleta es:", "Colocar de manera recta el arco de los pies en los apoyapiés."),
    ("Para un frenado seguro de la motocicleta (en un frenado usual como, al entrar a una curva, al llegar a una intersección, etc.), se debe utilizar:", "El freno delantero y el freno posterior."),
    ("Al realizar el cambio de carril, la conducta correcta es:", "Las alternativas a y c son correctas."),
    ("Mientras se conduce para alcanzar la velocidad deseada, la aceleración debe ser:", "Progresiva."),
]

# Preguntas que tienen imágenes en el PDF (número de pregunta del balotario, 1-indexed)
preguntas_con_imagen = {
    3, 8, 17, 30, 31, 32, 33, 39, 47, 63, 87, 92, 93, 94, 95, 96, 97, 98,
    99, 100, 101, 102, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
    114, 115, 116, 118, 119, 120, 121, 122, 123, 124, 125, 126, 128, 129,
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 144, 164,
    165, 170, 179, 181, 182, 195
}

print(f"Total preguntas definidas: {len(qa_pairs)}")
print(f"Preguntas con imagen: {len(preguntas_con_imagen)}")

# Generate distractors for each question
random.seed(42)
all_answers = [a for _, a in qa_pairs]

js_lines = ['const PREGUNTAS_BANCO = [']
for idx, (q, correct) in enumerate(qa_pairs):
    num_pregunta = idx + 1  # 1-indexed question number

    wrong = []
    attempts = 0
    used = {correct}
    while len(wrong) < 2 and attempts < 200:
        candidate = random.choice(all_answers)
        if candidate not in used and len(candidate) < 250:
            wrong.append(candidate)
            used.add(candidate)
        attempts += 1
    while len(wrong) < 2:
        wrong.append("Ninguna de las anteriores.")

    options = [correct] + wrong
    random.shuffle(options)
    ci = options.index(correct)

    esc = lambda s: s.replace('\\', '\\\\').replace('"', '\\"')
    opts_str = ', '.join([f'"{esc(o)}"' for o in options])

    # Add imagen field if this question has an image
    img_field = ""
    if num_pregunta in preguntas_con_imagen:
        img_field = f', imagen: "imagenes/pregunta_{num_pregunta}.png"'

    js_lines.append(f'  {{ id: {num_pregunta}, pregunta: "{esc(q)}", opciones: [{opts_str}], correcta: {ci}{img_field} }},')

js_lines.append('];')

with open('preguntas.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

print(f"preguntas.js generado exitosamente con {len(qa_pairs)} preguntas")
print(f"De las cuales {len(preguntas_con_imagen)} tienen campo de imagen")
