# Servicio de Perfiles SENCE

API REST para el servicio de Perfiles de SENCE, que permite gestionar perfiles de usuarios, funciones y permisos en los sistemas de SENCE.

## Descripción

Este servicio actúa como una capa intermedia entre aplicaciones REST y el servicio SOAP de Perfiles de SENCE, facilitando la gestión de usuarios, perfiles, funciones y permisos mediante endpoints REST modernos.

## Endpoints Disponibles

### GET `/api/v1/perfiles/usuarios`

Consulta usuarios (Personas Naturales) por perfil y sistema.

#### Query Parameters

- **id_sistema** (integer, requerido): ID del sistema
- **id_perfil** (integer, requerido): ID del perfil

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "usuario": [
    {
      "idUsuario": 1,
      "nombre": "Juan Carlos",
      "apellidoPaterno": "Pérez",
      "apellidoMaterno": "González",
      "tipoPersona": "PersonaNatural"
    }
  ]
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/usuarios?id_sistema=1&id_perfil=2"
```

---

### GET `/api/v1/perfiles/usuarios/{rut}`

Consulta todos los perfiles que posee un usuario según su RUT en un sistema particular.

#### Path Parameters

- **rut** (integer, requerido): RUT del usuario (sin puntos ni guión)

#### Query Parameters

- **id_sistema** (integer, requerido): ID del sistema
- **tipo_persona** (string, requerido): Tipo de persona (PersonaNatural, PersonaJuridica, PersonaExtranjera, Otra)

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "perfil": {
    "idSistema": 1,
    "nombreSistema": "Sistema de Capacitación",
    "perfil": [
      {
        "idPerfil": 2,
        "nombrePerfil": "Ejecutivo OTEC",
        "estado": "Activo",
        "tipoPerfil": "Normal",
        "region": "Region_Metropolitana_de_Santiago",
        "funcion": [
          {
            "idFuncion": 10,
            "nombreFuncion": "Registrar curso",
            "obligatorio": true,
            "denegado": false,
            "estado": "Activo"
          }
        ]
      }
    ]
  }
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/usuarios/12345678?id_sistema=1&tipo_persona=PersonaNatural"
```

---

### GET `/api/v1/perfiles/perfiles`

Consulta la lista de perfiles asociados a un sistema.

#### Query Parameters

- **id_sistema** (integer, requerido): ID del sistema

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "perfil": {
    "idSistema": 1,
    "nombreSistema": "Sistema de Capacitación",
    "perfil": [
      {
        "idPerfil": 1,
        "nombrePerfil": "Administrador",
        "estado": "Activo",
        "tipoPerfil": "Administrador",
        "region": null
      },
      {
        "idPerfil": 2,
        "nombrePerfil": "Ejecutivo OTEC",
        "estado": "Activo",
        "tipoPerfil": "Normal",
        "region": "Region_Metropolitana_de_Santiago"
      }
    ]
  }
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/perfiles?id_sistema=1"
```

---

### GET `/api/v1/perfiles/funciones`

Consulta el listado de funciones disponibles de un sistema.

#### Query Parameters

- **id_sistema** (integer, requerido): ID del sistema

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "funcion": [
    {
      "idFuncion": 10,
      "nombreFuncion": "Registrar curso",
      "obligatorio": true,
      "denegado": false,
      "estado": "Activo"
    },
    {
      "idFuncion": 11,
      "nombreFuncion": "Modificar curso",
      "obligatorio": false,
      "denegado": false,
      "estado": "Activo"
    }
  ]
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/funciones?id_sistema=1"
```

---

### GET `/api/v1/perfiles/funciones/por-perfil`

Consulta el listado de funciones que tiene un perfil asociado a un sistema.

#### Query Parameters

- **id_perfil** (integer, requerido): ID del perfil
- **id_sistema** (integer, requerido): ID del sistema

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "funcion": [
    {
      "idFuncion": 10,
      "nombreFuncion": "Registrar curso",
      "obligatorio": true,
      "denegado": false,
      "estado": "Activo"
    }
  ]
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/funciones/por-perfil?id_perfil=2&id_sistema=1"
```

---

### GET `/api/v1/perfiles/empresas`

Consulta usuarios (Personas Jurídicas) por perfil y sistema.

#### Query Parameters

- **id_sistema** (integer, requerido): ID del sistema
- **id_perfil** (integer, requerido): ID del perfil

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Acceso autorizado"
  },
  "usuarioEmpresa": [
    {
      "idUsuarioEmpresa": 1,
      "razonSocial": "Empresa de Capacitación S.A.",
      "tipoEmpresa": "OTEC",
      "tipoPersona": "PersonaJuridica"
    }
  ]
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/perfiles/empresas?id_sistema=1&id_perfil=3"
```

---

### POST `/api/v1/perfiles/solicitar`

Solicita la asignación de un perfil para un usuario de un sistema particular.

#### Request Body

```json
{
  "idSistema": 1,
  "idPerfil": 2,
  "rutUsuario": 12345678,
  "motivoSolicitud": "Nuevo ejecutivo OTEC",
  "idRegion": 13,
  "tipoPersona": "PersonaNatural",
  "rutUsrUpdate": 87654321
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **idPerfil** (integer, requerido): ID del perfil a solicitar
- **rutUsuario** (integer, requerido): RUT del usuario (sin puntos ni guión)
- **motivoSolicitud** (string, opcional): Motivo de la solicitud
- **idRegion** (integer, requerido): ID de la región
- **tipoPersona** (string, requerido): Tipo de persona
- **rutUsrUpdate** (integer, requerido): RUT del usuario que realiza la solicitud

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Perfil solicitado correctamente"
  }
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/perfiles/solicitar" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "idPerfil": 2,
    "rutUsuario": 12345678,
    "motivoSolicitud": "Nuevo ejecutivo",
    "idRegion": 13,
    "tipoPersona": "PersonaNatural",
    "rutUsrUpdate": 87654321
  }'
```

---

### POST `/api/v1/perfiles/bloquear`

Bloquea el perfil de un usuario en un sistema.

#### Request Body

```json
{
  "idSistema": 1,
  "idPerfil": 2,
  "rutUsuario": 12345678,
  "tipoPersona": "PersonaNatural",
  "rutUsrUpdate": 87654321
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **idPerfil** (integer, requerido): ID del perfil a bloquear
- **rutUsuario** (integer, requerido): RUT del usuario (sin puntos ni guión)
- **tipoPersona** (string, requerido): Tipo de persona
- **rutUsrUpdate** (integer, requerido): RUT del usuario que realiza el bloqueo

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Perfil bloqueado correctamente"
  }
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/perfiles/bloquear" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "idPerfil": 2,
    "rutUsuario": 12345678,
    "tipoPersona": "PersonaNatural",
    "rutUsrUpdate": 87654321
  }'
```

---

### POST `/api/v1/perfiles/asignar`

Asigna un perfil a un usuario en un sistema.

#### Request Body

```json
{
  "idSistema": 1,
  "idPerfil": 2,
  "region": "Region_Metropolitana_de_Santiago",
  "rutUsuario": 12345678,
  "tipoPersona": "PersonaNatural",
  "rutUsrUpdate": 87654321
}
```

#### Parámetros

- **idSistema** (integer, requerido): ID del sistema
- **idPerfil** (integer, requerido): ID del perfil a asignar
- **region** (string, requerido): Código de región
- **rutUsuario** (integer, requerido): RUT del usuario (sin puntos ni guión)
- **tipoPersona** (string, requerido): Tipo de persona
- **rutUsrUpdate** (integer, requerido): RUT del usuario que realiza la asignación

#### Response 200 OK

```json
{
  "autorizacion": {
    "acceso": "Autorizado",
    "codigo": 200,
    "descripcion": "Perfil asignado correctamente"
  }
}
```

#### Ejemplo de Uso

```bash
curl -X POST "http://localhost:8000/api/v1/perfiles/asignar" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "idPerfil": 2,
    "region": "Region_Metropolitana_de_Santiago",
    "rutUsuario": 12345678,
    "tipoPersona": "PersonaNatural",
    "rutUsrUpdate": 87654321
  }'
```

---

## Tipos de Persona (ETipoPersona)

- `PersonaNatural`: Persona natural/física
- `PersonaJuridica`: Persona jurídica/empresa
- `PersonaExtranjera`: Persona extranjera
- `Otra`: Otro tipo de persona

## Estados (EEstado)

- `Activo`: Perfil o función activa
- `Inactivo`: Perfil o función inactiva

## Tipos de Perfil (ETipoPerfil)

- `Normal`: Perfil normal de usuario
- `Administrador`: Perfil de administrador
- `ArquitectoTi`: Perfil de arquitecto TI
- `Sence`: Perfil especial de SENCE

## Regiones de Chile (ERegion)

- `Region_de_Tarapaca`: Región de Tarapacá (I)
- `Region_de_Antofagasta`: Región de Antofagasta (II)
- `Region_de_Atacama`: Región de Atacama (III)
- `Region_de_Coquimbo`: Región de Coquimbo (IV)
- `Region_de_Valparaiso`: Región de Valparaíso (V)
- `Region_del_Lib_Gen_Ber_Ohig`: Región del Libertador General Bernardo O'Higgins (VI)
- `Region_del_Maule`: Región del Maule (VII)
- `Region_del_Bio_Bio`: Región del Biobío (VIII)
- `Region_de_la_Araucania`: Región de La Araucanía (IX)
- `Region_de_los_Lagos`: Región de Los Lagos (X)
- `Region_de_Aysen_del_Gen_Carlos_IC`: Región de Aysén del General Carlos Ibáñez del Campo (XI)
- `Region_de_Magallanes_y_la_Ant_Chilena`: Región de Magallanes y de la Antártica Chilena (XII)
- `Region_Metropolitana_de_Santiago`: Región Metropolitana de Santiago (XIII)
- `Region_de_los_Rios`: Región de Los Ríos (XIV)
- `Region_de_Arica_y_Parinacota`: Región de Arica y Parinacota (XV)
- `Region_de_Nuble`: Región de Ñuble (XVI)
- `Extranjero`: Extranjero

## Códigos de Estado HTTP

### Respuestas Exitosas

- **200 OK**: Operación exitosa

### Respuestas de Error

- **422 Unprocessable Entity**: Error de validación en los datos enviados
- **502 Bad Gateway**: Error en la comunicación con el servicio SOAP

## Ejemplos de Uso Completos

### Ejemplo Python: Consultar perfiles de un usuario

```python
import requests

# Consultar perfiles de un usuario
rut = 12345678
id_sistema = 1
tipo_persona = "PersonaNatural"

response = requests.get(
    f"http://localhost:8000/api/v1/perfiles/usuarios/{rut}",
    params={
        "id_sistema": id_sistema,
        "tipo_persona": tipo_persona
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Usuario tiene {len(data['perfil']['perfil'])} perfiles")
    for perfil in data['perfil']['perfil']:
        print(f"- {perfil['nombrePerfil']} ({perfil['estado']})")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Ejemplo Python: Asignar perfil a usuario

```python
import requests

# Asignar perfil
payload = {
    "idSistema": 1,
    "idPerfil": 2,
    "region": "Region_Metropolitana_de_Santiago",
    "rutUsuario": 12345678,
    "tipoPersona": "PersonaNatural",
    "rutUsrUpdate": 87654321
}

response = requests.post(
    "http://localhost:8000/api/v1/perfiles/asignar",
    json=payload
)

if response.status_code == 200:
    data = response.json()
    print(f"Perfil asignado: {data['autorizacion']['descripcion']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Ejemplo JavaScript: Consultar funciones de un perfil

```javascript
const idSistema = 1;
const idPerfil = 2;

fetch(`http://localhost:8000/api/v1/perfiles/funciones/por-perfil?id_sistema=${idSistema}&id_perfil=${idPerfil}`)
  .then(response => response.json())
  .then(data => {
    console.log(`Perfil tiene ${data.funcion.length} funciones`);
    data.funcion.forEach(func => {
      console.log(`- ${func.nombreFuncion} (${func.estado})`);
    });
  })
  .catch(error => console.error('Error:', error));
```

### Ejemplo JavaScript: Solicitar perfil

```javascript
const payload = {
  idSistema: 1,
  idPerfil: 2,
  rutUsuario: 12345678,
  motivoSolicitud: "Nuevo ejecutivo OTEC",
  idRegion: 13,
  tipoPersona: "PersonaNatural",
  rutUsrUpdate: 87654321
};

fetch('http://localhost:8000/api/v1/perfiles/solicitar', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(data => {
    console.log('Perfil solicitado:', data.autorizacion.descripcion);
  })
  .catch(error => console.error('Error:', error));
```

## Consideraciones Importantes

### Formato del RUT

- Los RUT deben enviarse **sin puntos ni guión**, solo números
- Ejemplo: `12345678` (no `12.345.678-9`)
- El dígito verificador no se incluye

### Autorización

Todos los endpoints retornan un objeto `autorizacion` con:
- `acceso`: Estado del acceso (Autorizado/NoAutorizado)
- `codigo`: Código de respuesta
- `descripcion`: Descripción del resultado

### Gestión de Perfiles

1. **Solicitar**: Crea una solicitud de perfil que debe ser aprobada
2. **Asignar**: Asigna directamente un perfil (requiere permisos)
3. **Bloquear**: Desactiva un perfil asignado

### Regiones

- Los IDs de región corresponden a los códigos oficiales de Chile
- La región es obligatoria al asignar ciertos tipos de perfiles
- Algunas funciones pueden estar restringidas por región

## Manejo de Errores

### Error 422: Validación

```json
{
  "detail": [
    {
      "loc": ["body", "rutUsuario"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solución**: Verificar que todos los campos requeridos estén presentes y con el tipo correcto.

### Error 502: SOAP Fault

```json
{
  "success": false,
  "mensaje": "Error en el servicio SOAP",
  "codigo_error": "SOAP_FAULT",
  "detalle": "Fault code: ..."
}
```

**Solución**: 
1. Verificar conectividad con el servicio SOAP
2. Verificar que el usuario tenga permisos
3. Revisar los logs en `logs/app.log`

### Error: Usuario sin perfiles

```json
{
  "autorizacion": {
    "acceso": "NoAutorizado",
    "codigo": 404,
    "descripcion": "Usuario no tiene perfiles asignados"
  }
}
```

**Solución**: El usuario no tiene perfiles en el sistema. Puede solicitar un perfil usando el endpoint `/perfiles/solicitar`.

## Variables de Entorno

Configurar en el archivo `.env`:

```env
# Configuración del servicio SOAP de Perfiles
USE_SOAP_MOCKS=false
SOAP_TIMEOUT=30
```

## Testing

Para ejecutar los tests de este servicio:

```bash
pytest tests/test_perfiles.py -v
```

## Troubleshooting

### Problema: "Usuario no encontrado"

**Causa**: El RUT no existe en el sistema

**Solución**: Verificar que el usuario esté registrado previamente

### Problema: "Perfil no disponible"

**Causa**: El perfil no existe o está inactivo

**Solución**: Consultar perfiles disponibles con `/perfiles/perfiles`

### Problema: "Región inválida"

**Causa**: El código de región no es válido

**Solución**: Usar uno de los códigos de región listados en la documentación

### Problema: "Tipo de persona no coincide"

**Causa**: El tipo de persona no corresponde al RUT

**Solución**: Verificar que PersonaNatural se use para personas y PersonaJuridica para empresas

## Casos de Uso Típicos

### 1. Onboarding de Nuevo Usuario

```python
# 1. Consultar perfiles disponibles
perfiles_response = requests.get(
    "http://localhost:8000/api/v1/perfiles/perfiles",
    params={"id_sistema": 1}
)

# 2. Solicitar perfil
solicitud_response = requests.post(
    "http://localhost:8000/api/v1/perfiles/solicitar",
    json={
        "idSistema": 1,
        "idPerfil": 2,
        "rutUsuario": 12345678,
        "motivoSolicitud": "Nuevo ejecutivo",
        "idRegion": 13,
        "tipoPersona": "PersonaNatural",
        "rutUsrUpdate": 87654321
    }
)
```

### 2. Verificar Permisos de Usuario

```python
# Obtener perfiles y funciones del usuario
response = requests.get(
    f"http://localhost:8000/api/v1/perfiles/usuarios/{rut}",
    params={
        "id_sistema": 1,
        "tipo_persona": "PersonaNatural"
    }
)

# Verificar si tiene función específica
data = response.json()
tiene_permiso = any(
    f['nombreFuncion'] == 'Registrar curso' 
    for perfil in data['perfil']['perfil']
    for f in perfil.get('funcion', [])
)
```

### 3. Gestión de Perfiles por Administrador

```python
# 1. Listar usuarios con cierto perfil
usuarios = requests.get(
    "http://localhost:8000/api/v1/perfiles/usuarios",
    params={"id_sistema": 1, "id_perfil": 2}
)

# 2. Bloquear usuario específico
bloquear = requests.post(
    "http://localhost:8000/api/v1/perfiles/bloquear",
    json={
        "idSistema": 1,
        "idPerfil": 2,
        "rutUsuario": 12345678,
        "tipoPersona": "PersonaNatural",
        "rutUsrUpdate": 87654321
    }
)
```

## Soporte

Para más información sobre el servicio SOAP subyacente, consulte la documentación oficial de SENCE.

## Changelog

- **v1.0.0**: Implementación inicial del servicio de Perfiles
  - 9 endpoints REST
  - Gestión completa de perfiles, usuarios y funciones
  - Soporte para personas naturales y jurídicas
  - Validaciones y manejo de errores robusto

