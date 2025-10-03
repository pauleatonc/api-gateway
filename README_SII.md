# Servicio de Impuestos Internos (SII)

API REST para el servicio del Servicio de Impuestos Internos de Chile, que permite consultar información tributaria y empresarial de contribuyentes.

## Descripción

Este servicio actúa como una capa intermedia entre aplicaciones REST y el servicio SOAP del SII, facilitando la consulta de información tributaria mediante endpoints REST modernos.

## Endpoints Disponibles

### POST `/api/v1/sii/representante-legal`

Consulta el representante legal vigente de un RUT.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": "12345678",
  "dv": "9"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (string, opcional): RUT del contribuyente (sin puntos ni guión)
- **dv** (string, opcional): Dígito verificador

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "representantes": [
      {
        "rut": 98765432,
        "dv": "1",
        "fechaInicio": "2020-01-15"
      }
    ],
    "datosGenerales": {
      "fechaInicioActividad": "2015-03-01T00:00:00",
      "glosa": "Vigente",
      "estado": "ACTIVO"
    }
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/representante-legal" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": "12345678",
    "dv": "9"
  }'
```

---

### POST `/api/v1/sii/relacion-empresa`

Verifica si un contribuyente es socio de una empresa.

#### Request Body

```json
{
  "idSistema": 1,
  "rutEmp": 12345678,
  "dvEmp": "9",
  "rutSoc": 87654321,
  "dvSoc": "0"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rutEmp** (integer, requerido): RUT de la empresa (sin puntos ni guión)
- **dvEmp** (string, opcional): Dígito verificador de la empresa
- **rutSoc** (integer, requerido): RUT del socio
- **dvSoc** (string, opcional): Dígito verificador del socio

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Es socio de la empresa",
    "estado": "VIGENTE"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/relacion-empresa" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rutEmp": 12345678,
    "dvEmp": "9",
    "rutSoc": 87654321,
    "dvSoc": "0"
  }'
```

---

### POST `/api/v1/sii/movimiento-contribuyente`

Verifica si un contribuyente presenta movimiento tributario.

#### Request Body

```json
{
  "idSistema": 1,
  "rutCont": 12345678,
  "dvCont": "9",
  "periodoTrib": "202312"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rutCont** (integer, requerido): RUT del contribuyente
- **dvCont** (string, opcional): Dígito verificador
- **periodoTrib** (string, opcional): Período tributario (formato AAAAMM)

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Presenta movimiento",
    "estado": "CON_MOVIMIENTO"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/movimiento-contribuyente" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rutCont": 12345678,
    "dvCont": "9",
    "periodoTrib": "202312"
  }'
```

---

### POST `/api/v1/sii/numero-empleados`

Consulta la cantidad de empleados de una empresa.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9",
  "periodo": 202312
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT de la empresa
- **dv** (string, opcional): Dígito verificador
- **periodo** (integer, requerido): Período de consulta (formato AAAAMM)

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Consulta exitosa",
    "estado": "ACTIVO",
    "numeroEmpleados": "25"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/numero-empleados" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9",
    "periodo": 202312
  }'
```

---

### POST `/api/v1/sii/categoria-empresa`

Consulta la categorización de una empresa según el monto de sus ventas.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9",
  "fecha": "2023-12-01T00:00:00",
  "tipoConsulta": 1
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT de la empresa
- **dv** (string, opcional): Dígito verificador
- **fecha** (datetime, requerido): Fecha de consulta
- **tipoConsulta** (integer, requerido): Tipo de consulta (1-4)

**Tipos de Consulta:**
- `1`: Microempresa
- `2`: Pequeña empresa
- `3`: Mediana empresa
- `4`: Grande empresa

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Empresa clasificada",
    "estado": "ACTIVO",
    "tipo": "2",
    "glosaTipo": "Pequeña empresa",
    "cantPeriodo": "12"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/categoria-empresa" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9",
    "fecha": "2023-12-01T00:00:00",
    "tipoConsulta": 1
  }'
```

---

### POST `/api/v1/sii/datos-contribuyente`

Obtiene los datos personales del contribuyente (Persona Natural o Jurídica).

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT del contribuyente
- **dv** (string, opcional): Dígito verificador

#### Response 200 OK

Para **Persona Natural**:
```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "estado": "ACTIVO",
    "glosa": "Contribuyente vigente",
    "nombre": "Juan Carlos",
    "apPaterno": "Pérez",
    "apMaterno": "González",
    "xml": "..."
  },
  "xmlRespuesta": "..."
}
```

Para **Persona Jurídica**:
```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "estado": "ACTIVO",
    "glosa": "Contribuyente vigente",
    "razonSocial": "Empresa de Capacitación S.A.",
    "xml": "..."
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/datos-contribuyente" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9"
  }'
```

---

### POST `/api/v1/sii/actividad-economica`

Informa las actividades económicas asociadas a un contribuyente.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT del contribuyente
- **dv** (string, opcional): Dígito verificador

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Consulta exitosa",
    "estado": "ACTIVO",
    "actividadEconomica": [
      {
        "actividad": 854910,
        "categoria": 1,
        "descripcion": "Enseñanza de capacitación técnica",
        "fechaInic": "2015-03-01T00:00:00"
      },
      {
        "actividad": 702001,
        "categoria": 2,
        "descripcion": "Consultorías",
        "fechaInic": "2018-06-15T00:00:00"
      }
    ]
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/actividad-economica" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9"
  }'
```

---

### POST `/api/v1/sii/estado-giro`

Consulta el estado del giro de un contribuyente.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT del contribuyente
- **dv** (string, opcional): Dígito verificador

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Giro vigente",
    "estado": "ACTIVO"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/estado-giro" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9"
  }'
```

---

### POST `/api/v1/sii/fecha-inicio-actividad`

Consulta la fecha de inicio de actividades de un contribuyente.

#### Request Body

```json
{
  "idSistema": 1,
  "rut": 12345678,
  "dv": "9"
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **rut** (integer, requerido): RUT del contribuyente
- **dv** (string, opcional): Dígito verificador

#### Response 200 OK

```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "fechaInicioActividad": "2015-03-01T00:00:00",
    "glosa": "Fecha obtenida correctamente",
    "estado": "ACTIVO"
  },
  "xmlRespuesta": "..."
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/sii/fecha-inicio-actividad" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "rut": 12345678,
    "dv": "9"
  }'
```

---

## Estados del Proceso (ETipoEstado)

Todos los endpoints retornan un estado del proceso en la cabecera:

- `CORRECTO`: Consulta exitosa
- `INCORRECTO`: Datos incorrectos
- `ERROR`: Error en el proceso
- `EXCEPCION`: Excepción en el servicio
- `PROCESAR`: En proceso
- `NULO`: Estado nulo

## Formato de RUT

- Los RUT deben enviarse **sin puntos**, solo números
- El dígito verificador es opcional pero recomendado
- Ejemplo: `rut: 12345678`, `dv: "9"` (no `12.345.678-9`)

## Formato de Período

Para consultas con período:
- Formato: `AAAAMM`
- Ejemplo: `202312` (diciembre 2023)
- Rango válido: `200001` a `999912`

## Códigos de Estado HTTP

### Respuestas Exitosas

- **200 OK**: Consulta exitosa

### Respuestas de Error

- **422 Unprocessable Entity**: Error de validación
- **502 Bad Gateway**: Error del servicio SOAP

## Ejemplos de Uso Completos

### Ejemplo Python: Consultar datos completos de una empresa

```python
import requests

# Datos de la empresa
rut_empresa = 12345678
dv = "9"
id_sistema = 1

# 1. Datos básicos del contribuyente
datos_response = requests.post(
    "http://localhost:8000/api/v1/sii/datos-contribuyente",
    json={
        "idSistema": id_sistema,
        "rut": rut_empresa,
        "dv": dv
    }
)

if datos_response.status_code == 200:
    datos = datos_response.json()
    print(f"Razón Social: {datos['respuesta'].get('razonSocial')}")
    print(f"Estado: {datos['respuesta']['estado']}")

# 2. Actividades económicas
actividades_response = requests.post(
    "http://localhost:8000/api/v1/sii/actividad-economica",
    json={
        "idSistema": id_sistema,
        "rut": rut_empresa,
        "dv": dv
    }
)

if actividades_response.status_code == 200:
    actividades = actividades_response.json()
    print(f"\nActividades Económicas:")
    for act in actividades['respuesta']['actividadEconomica']:
        print(f"- {act['descripcion']} (Código: {act['actividad']})")

# 3. Representante legal
representante_response = requests.post(
    "http://localhost:8000/api/v1/sii/representante-legal",
    json={
        "idSistema": id_sistema,
        "rut": str(rut_empresa),
        "dv": dv
    }
)

if representante_response.status_code == 200:
    representante = representante_response.json()
    print(f"\nRepresentantes Legales:")
    for rep in representante['respuesta']['representantes']:
        print(f"- RUT: {rep['rut']}-{rep['dv']}")

# 4. Número de empleados (período actual)
periodo = 202312
empleados_response = requests.post(
    "http://localhost:8000/api/v1/sii/numero-empleados",
    json={
        "idSistema": id_sistema,
        "rut": rut_empresa,
        "dv": dv,
        "periodo": periodo
    }
)

if empleados_response.status_code == 200:
    empleados = empleados_response.json()
    print(f"\nNúmero de Empleados: {empleados['respuesta']['numeroEmpleados']}")
```

### Ejemplo Python: Verificar si un socio pertenece a una empresa

```python
import requests

# Verificar relación socio-empresa
payload = {
    "idSistema": 1,
    "rutEmp": 12345678,  # RUT empresa
    "dvEmp": "9",
    "rutSoc": 87654321,  # RUT socio
    "dvSoc": "0"
}

response = requests.post(
    "http://localhost:8000/api/v1/sii/relacion-empresa",
    json=payload
)

if response.status_code == 200:
    data = response.json()
    if data['cabecera']['estadoProceso'] == 'CORRECTO':
        print(f"Relación: {data['respuesta']['glosa']}")
        print(f"Estado: {data['respuesta']['estado']}")
    else:
        print(f"Error: {data['cabecera']['respuestaProceso']}")
else:
    print(f"Error HTTP: {response.status_code}")
```

### Ejemplo JavaScript: Consultar categoría de empresa

```javascript
const payload = {
  idSistema: 1,
  rut: 12345678,
  dv: "9",
  fecha: "2023-12-01T00:00:00",
  tipoConsulta: 1
};

fetch('http://localhost:8000/api/v1/sii/categoria-empresa', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(data => {
    if (data.cabecera.estadoProceso === 'CORRECTO') {
      console.log(`Categoría: ${data.respuesta.glosaTipo}`);
      console.log(`Tipo: ${data.respuesta.tipo}`);
    } else {
      console.log(`Error: ${data.cabecera.respuestaProceso}`);
    }
  })
  .catch(error => console.error('Error:', error));
```

### Ejemplo JavaScript: Consultar actividades económicas

```javascript
const consultarActividades = async (rut, dv) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/sii/actividad-economica', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        idSistema: 1,
        rut: rut,
        dv: dv
      })
    });
    
    const data = await response.json();
    
    if (data.cabecera.estadoProceso === 'CORRECTO') {
      console.log('Actividades Económicas:');
      data.respuesta.actividadEconomica.forEach(act => {
        console.log(`- ${act.descripcion} (${act.actividad})`);
        console.log(`  Categoría: ${act.categoria}`);
        console.log(`  Inicio: ${new Date(act.fechaInic).toLocaleDateString()}`);
      });
    }
  } catch (error) {
    console.error('Error:', error);
  }
};

consultarActividades(12345678, '9');
```

## Consideraciones Importantes

### Formato de RUT

- RUT sin puntos ni guión (solo números)
- Dígito verificador como string separado
- RUT válido: entre 7 y 8 dígitos (10.000.000 a 99.999.999)

### Formato de Fechas

- Las fechas se retornan en formato ISO 8601: `YYYY-MM-DDTHH:mm:ss`
- Para enviar fechas, usar el mismo formato

### Período Tributario

- Formato `AAAAMM` (año y mes sin separadores)
- Ejemplo: `202312` = Diciembre 2023
- Validación: mes debe ser 01-12

### Tipos de Consulta de Categoría

1. **Microempresa**: Ventas anuales menores a UF 2.400
2. **Pequeña empresa**: Ventas anuales entre UF 2.400 y UF 25.000
3. **Mediana empresa**: Ventas anuales entre UF 25.000 y UF 100.000
4. **Grande empresa**: Ventas anuales superiores a UF 100.000

### Códigos de Actividad Económica

Los códigos siguen la clasificación CIIU (Clasificación Industrial Internacional Uniforme)
- Ejemplo: `854910` = Enseñanza de capacitación técnica

## Manejo de Errores

### Error 422: Validación

```json
{
  "detail": [
    {
      "loc": ["body", "rut"],
      "msg": "El RUT debe tener entre 7 y 8 dígitos",
      "type": "value_error"
    }
  ]
}
```

**Solución**: Verificar que el RUT tenga el formato correcto (7-8 dígitos).

### Error 502: SOAP Fault

```bash
{
  "detail": "Error en el servicio SOAP"
}
```

**Solución**: 
1. Verificar conectividad con el SII
2. Verificar que el RUT exista en los registros del SII
3. Revisar logs en `logs/app.log`

### Contribuyente no encontrado

```json
{
  "cabecera": {
    "estadoProceso": "INCORRECTO",
    "respuestaProceso": "RUT no existe",
    "codigoProceso": 404
  }
}
```

**Solución**: Verificar que el RUT sea válido y esté inscrito en el SII.

## Casos de Uso Típicos

### 1. Validación de Empresa para Capacitación

```python
def validar_empresa_otec(rut, dv):
    """Valida que una empresa cumpla requisitos para ser OTEC"""
    
    # 1. Verificar que existe y está activa
    datos = consultar_datos_contribuyente(rut, dv)
    if datos['respuesta']['estado'] != 'ACTIVO':
        return False, "Empresa no está activa"
    
    # 2. Verificar actividad económica relacionada con capacitación
    actividades = consultar_actividad_economica(rut, dv)
    codigos_capacitacion = [854910, 854920]
    tiene_actividad = any(
        act['actividad'] in codigos_capacitacion 
        for act in actividades['respuesta']['actividadEconomica']
    )
    if not tiene_actividad:
        return False, "No tiene actividad de capacitación"
    
    # 3. Verificar número mínimo de empleados
    empleados = consultar_numero_empleados(rut, dv, 202312)
    num_empleados = int(empleados['respuesta']['numeroEmpleados'])
    if num_empleados < 5:
        return False, "Número insuficiente de empleados"
    
    return True, "Empresa válida para OTEC"
```

### 2. Perfil Completo de Empresa

```python
def obtener_perfil_completo(rut, dv):
    """Obtiene perfil completo de una empresa"""
    perfil = {}
    
    # Datos básicos
    datos = consultar_datos_contribuyente(rut, dv)
    perfil['razonSocial'] = datos['respuesta'].get('razonSocial')
    perfil['estado'] = datos['respuesta']['estado']
    
    # Fecha inicio actividades
    inicio = consultar_fecha_inicio_actividad(rut, dv)
    perfil['inicioActividades'] = inicio['respuesta']['fechaInicioActividad']
    
    # Actividades económicas
    actividades = consultar_actividad_economica(rut, dv)
    perfil['actividades'] = [
        {
            'codigo': act['actividad'],
            'descripcion': act['descripcion'],
            'categoria': act['categoria']
        }
        for act in actividades['respuesta']['actividadEconomica']
    ]
    
    # Representantes legales
    representantes = consultar_representante_legal(str(rut), dv)
    perfil['representantes'] = [
        f"{rep['rut']}-{rep['dv']}"
        for rep in representantes['respuesta']['representantes']
    ]
    
    # Categoría empresa
    categoria = consultar_categoria_empresa(rut, dv, datetime.now(), 1)
    perfil['categoria'] = categoria['respuesta']['glosaTipo']
    
    return perfil
```

### 3. Verificación de Socio

```python
def verificar_socio_empresa(rut_empresa, dv_empresa, rut_socio, dv_socio):
    """Verifica si una persona es socio de una empresa"""
    
    relacion = consultar_relacion_contribuyente_empresa(
        rut_empresa, dv_empresa, rut_socio, dv_socio
    )
    
    if relacion['cabecera']['estadoProceso'] == 'CORRECTO':
        return {
            'es_socio': 'socio' in relacion['respuesta']['glosa'].lower(),
            'estado': relacion['respuesta']['estado'],
            'glosa': relacion['respuesta']['glosa']
        }
    else:
        return {
            'es_socio': False,
            'error': relacion['cabecera']['respuestaProceso']
        }
```

## Variables de Entorno

Configurar en el archivo `.env`:

```env
# Configuración del servicio SOAP del SII
USE_SOAP_MOCKS=false
SOAP_TIMEOUT=30
```

## Testing

Para ejecutar los tests de este servicio:

```bash
pytest tests/test_sii.py -v
```

## Troubleshooting

### Problema: "RUT no válido"

**Causa**: El RUT no cumple con el formato o validación

**Solución**: 
- Verificar que sean solo números (sin puntos ni guión)
- Verificar que tenga entre 7 y 8 dígitos
- El dígito verificador debe ser un solo carácter

### Problema: "Período inválido"

**Causa**: El formato del período no es correcto

**Solución**: Usar formato `AAAAMM` (ej: `202312`)

### Problema: "Contribuyente no encontrado"

**Causa**: El RUT no existe en los registros del SII

**Solución**: Verificar que el RUT esté inscrito en el SII

### Problema: "Sin información para el período"

**Causa**: No hay datos disponibles para ese período específico

**Solución**: Consultar con un período más reciente

## Límites y Restricciones

### Límites del Servicio

- Timeout: 30 segundos por defecto
- El SII puede tener restricciones de rate limiting
- Algunos datos pueden no estar disponibles para todos los contribuyentes

### Datos Sensibles

- La información tributaria es sensible
- Implementar autenticación apropiada en producción
- Registrar todos los accesos para auditoría
- Cumplir con normativas de protección de datos

## Soporte

Para más información sobre el servicio SOAP del SII, consulte la documentación oficial del Servicio de Impuestos Internos de Chile.

## Changelog

- **v1.0.0**: Implementación inicial del servicio SII
  - 9 endpoints de consulta
  - Consultas de datos tributarios y empresariales
  - Validaciones y manejo de errores robusto
  - Soporte para personas naturales y jurídicas

