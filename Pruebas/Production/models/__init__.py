# configuracion y tablas maestrras/temporales
from . import program_162_aprobador_config
from . import program_162_tmp_detalle
# el cabezal de la solicitud (necesita existir para la lineas y firmas)
from . import program_162_solicitud
# al final lo que depende directamente de la solicitud
from . import program_162_solicitud_line
from . import program_162_firma
# program 132 - turnos y configuracion de produccion
from . import program_132_turno_definicion
# dependen de la base  (horarios por sucursal  y config global)
from . import program_132_turno_horario
from . import program_132_produccion_config
# program 133 - catalogo de tipos de paradas de produccion
from . import program_133_paradas
# program 135 - catalogo de tipos de mermas de produccion
from . import program_135_mermas
# program 135 - registro transaccional de mermas
from . import program_135_merma_registro
# program 137 - catalogo de categorias de lineas de produccion
from . import program_137_categoria_linea
# sucursal
from . import sucursal
# program 138 - familia de produccion por sucursal
from . import program_138_familia

