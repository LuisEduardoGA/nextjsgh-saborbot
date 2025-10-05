# SaborBot
SaborBot 🤖

PWA de recetas con un chatbot que ayuda a buscar, filtrar y preparar platillos. Proyecto educativo/colaborativo construido con Next.js, TypeScript y Tailwind CSS.

Estado: En desarrollo (repositorio privado).

 * Objetivo del proyecto

Crear una aplicación web progresiva (PWA) que:

    1.- Permita buscar recetas por ingredientes, categoría, tiempo, dificultad, etc.
    2.- Tenga un chatbot que sugiera recetas y resuelva dudas (p. ej., sustituciones de ingredientes).
    3.- Funcione offline (caché de assets y recetas guardadas) y se pueda instalar en el dispositivo.

Funcionalidades (MVP)

- Buscador de recetas (por nombre/ingredientes).
- Chatbot con respuestas contextuales (API externa).
- Favoritos y listas (persistencia local).
- PWA (instalable) + soporte básico offline.
- Internacionalización básica (español primero).
- Más adelante: perfiles de usuario

Tecnologías:

* Frontend: Next.js (App Router), TypeScript, Tailwind CSS
* Build Dev: Turbopack (modo desarrollo)
* Estado / Datos: React hooks, fetch/axios
* Chat/Recetas (APIs): Por definir (p. ej., Spoonacular, TheMealDB, etc.)
* Calidad: ESLint + Prettier
* Gestión: Git + GitHub (PRs, issues)

Requisitos previos

    1.- Node.js 18 o 20 (LTS recomendado)
    2.- npm (incluido con Node) o pnpm/yarn si el equipo lo decide (por defecto usamos npm)
    3.- Git instalado
    4.- Acceso al repo privado como colaborador

🗂️ Estructura del proyecto (base)
.
├─ src/
│  ├─ app/
│  │  ├─ layout.tsx        # Layout raíz de la app
│  │  ├─ page.tsx          # Página principal ("/")
│  │  └─ api/              # Endpoints (si se necesitan)
│  ├─ components/          # Componentes reutilizables (UI)
│  ├─ lib/                 # Utilidades, helpers, clientes de APIs
│  ├─ styles/              # estilos globales (Tailwind)
│  └─ types/               # Tipos/Interfaces TS
├─ public/                 # Íconos, imágenes, manifest, etc.
├─ .env.local              # Variables de entorno (NO se sube)
├─ .gitignore
├─ package.json
└─ README.md

🔐 Variables de entorno

Crea un archivo .env.local en la raíz (nunca lo subas al repositorio).
Ejemplo de plantilla:

# APIs de recetas (ejemplo)
RECIPES_API_URL=https://api.ejemplo.com
RECIPES_API_KEY=tu_api_key_aqui

# Chatbot (ejemplo)
CHAT_API_URL=https://api.chatbot.com
CHAT_API_KEY=tu_api_key_chat_aqui


Si usas claves reales, compártelas por un canal seguro y no las pegues en el README ni en commits.

Scripts de npm

npm run dev → Levanta el servidor de desarrollo

npm run build → Compila la app para producción

npm run start → Sirve la app compilada

npm run lint → Revisa el código con ESLint


/***************************************************************************************/

 IMPORTANTE DESDE AQUÍ LO DEMAS SALTATELO SOLO ES INFROMACIÓN ADICIONAL

Clonar el repoositorio

git clone https://github.com/LuisEduardoGA/nextjsgh-saborbot.git
cd nextjsgh-saborbot

Instalar dependencias

npm install

Crear .env.local (copiar la plantilla de arriba y ajustar claves si aplica)

Crear tu rama de trabajo

********************  Nunca trabajes directamente en main.    ***********

git checkout -b tu-nombre-o-feature
# Ejemplos:
# git checkout -b julio-ui
# git checkout -b carlos-chatbot
# git checkout -b maria-recetas


Levantar en local

npm run dev
# Abre http://localhost:3000

Flujo de trabajo en equipo (Git/GitHub)

Antes de empezar cada día:

git checkout main
git pull origin main
git checkout tu-rama
git merge main   # trae lo último a tu rama


Durante el desarrollo:

# Guarda cambios en tu rama
git add .
git commit -m "feat(recetas): buscador por ingrediente"
git push origin tu-rama


Abrir un Pull Request (PR):

Ve a GitHub → verás el botón “Compare & pull request”.

Rellena el título y descripción (qué hiciste, cómo probarlo).

Pide revisión a alguien del equipo.

Al aprobarse y pasar checks, merge a main.

Después del merge:

git checkout main
git pull origin main

Convención de ramas y commits

Ramas:

nombre/apellido-feature o feature/nombre-corto
Ej.: feature/chatbot-ui, julio/pagina-recetas

Commits (sencillo estilo “Conventional Commits”):

feat: ... (nueva funcionalidad)

fix: ... (arreglo de bug)

docs: ... (documentación)

style: ... (formato, espacios, etc. sin cambiar lógica)

refactor: ... (reestructuras sin cambios de comportamiento)

chore: ... (tareas menores, deps, etc.)

Ejemplos:

feat(chat): agrega botón de enviar en el chat
fix(recetas): corrige filtro por tiempo de cocción
docs: actualiza pasos de instalación en README

Estilo y calidad

Usa TypeScript (tipos en src/types cuando tenga sentido).

Corre npm run lint antes de subir cambios.

Mantén componentes pequeños y reutilizables en src/components/.

Evita credenciales en el código. Usa .env.local.

🆘 Mini-guía de conflictos (merge conflicts)

Git te mostrará los archivos en conflicto.

Abre el archivo y busca marcadores:

<<<<<<< HEAD
(tu versión)
=======
(versión de main)
>>>>>>> main


Elige o combina lo correcto, borra los marcadores <<<<<<< ======= >>>>>>>.

Guarda y confirma:

git add archivo-conflictivo
git commit -m "fix: resuelve conflicto en X componente"
git push


Si se complica, pidan ayuda al equipo. Es normal al principio.

🧭 Guía rápida para crear una página/ruta nueva

Con App Router (Next.js moderno), cada carpeta con page.tsx es una ruta.

Ejemplo: crear /recetas

src/app/recetas/page.tsx


Contenido mínimo:

export default function RecetasPage() {
  return <h1>Recetas</h1>;
}


Ir a http://localhost:3000/recetas.

PWA (nota inicial)

La base del proyecto es Next.js. Para PWA completa (manifest, service worker, cache de rutas), evaluaremos integrar next-pwa o configuración propia.

Objetivo MVP: iconos en public/, un manifest.json básico y cache inicial.

Luego agregaremos cache selectivo de recetas favoritas para offline.

En esta fase, documentaremos aquí los pasos concretos cuando se integren.

Pruebas (opcional a corto plazo)

Si el equipo lo decide, podremos integrar Vitest/Jest + React Testing Library para componentes críticos (buscador, chatbot).

Roadmap corto (sugerido)

UI base: home, navbar, layout (responsivo)

Página /recetas con listado y filtro simple

Chatbot (UI + función mock) → luego conectar API real

Favoritos (localStorage)

Primeros pasos de PWA (manifest + iconos)

III Equipo

5 colaboradores (principiantes en Git/GitHub).

Rol general: cada quien trabaja en su rama y abre PR para revisión.

Comunicación: anotar en el PR cómo probar la funcionalidad.

? FAQ breve

¿No me sale la “página index”?
En Next.js moderno está en src/app/page.tsx.

¿No puedo pushear a main?
Correcto. Trabaja en tu rama y abre PR. Así evitamos romper el proyecto.

PowerShell me pide “InputObject” al crear README
Usa:

echo "# SaborBot" | Out-File -Encoding UTF8 README.md


¿Dónde pongo mis claves de API?
En .env.local (no se sube). Pide las claves a quien administre.

Licencia / uso

Repositorio privado con fines educativos. No distribuir sin autorización del equipo.

Checklist para nuevos integrantes

 Acceso confirmado al repo privado

 Clonado y npm install ejecutado

 .env.local creado

 Rama propia creada

 npm run dev funcionando en http://localhost:3000

 PR de prueba (cambio mínimo) aprobado