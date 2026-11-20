var e=`https://cdn.jsdelivr.net/pyodide/v314.0.7/full/`,t=`
let ready;
let runCode;
let missing;
let queue = Promise.resolve();
onmessage = ({ data }) => {
  queue = queue.then(() => handle(data));
};
const install = async (py, names) => {
  await py.loadPackage('micropip');
  await py.pyimport('micropip').install(names);
};
const handle = async ({ id, url, code, session, args = [], file, columns, color, prepare, packages = [] }) => {
  try {
    ready ??= import(url + 'pyodide.mjs')
      .then((m) => m.loadPyodide({ indexURL: url }))
      .then((py) => {
        // Not the reader's \`<exec>\`, so that the trimming of the traceback drops these frames.
        runCode = py.runPython(${JSON.stringify(`
import ast, os, sys, traceback
from pyodide.code import eval_code_async
def _scb_exit(e):
    if e.code is not None and not isinstance(e.code, int):
        print(e.code, file=sys.stderr)
def _scb_session(src, g):
    try:
        for node in ast.parse(src, '<stdin>').body:
            exec(compile(ast.Interactive([node]), '<stdin>', 'single'), g)
    except SystemExit as e:
        _scb_exit(e)
    except BaseException as e:
        tb = None if isinstance(e, SyntaxError) else e.__traceback__.tb_next
        traceback.print_exception(e.with_traceback(tb))
async def _scb_run(src, g, session, argv, columns, color):
    sys.argv = list(argv)
    if columns:
        os.environ['COLUMNS'] = str(columns)
    else:
        os.environ.pop('COLUMNS', None)
    # Rich and other libraries print colours only to a terminal, unless FORCE_COLOR is set.
    if color:
        os.environ['FORCE_COLOR'] = '1'
    else:
        os.environ.pop('FORCE_COLOR', None)
    # Rich reads COLUMNS and FORCE_COLOR once, for the console that it keeps.
    if 'rich' in sys.modules:
        sys.modules['rich']._console = None
    if session:
        return _scb_session(src, g)
    try:
        await eval_code_async(src, g)
    except SystemExit as e:
        _scb_exit(e)
_scb_run
`)}, { filename: '<scb>' });
        missing = py.runPython(${JSON.stringify(`
import importlib.util, sys
from pyodide.code import find_imports
def _scb_missing(src):
    try:
        names = find_imports(src)
    except SyntaxError:
        return []
    return [n for n in names if n not in sys.stdlib_module_names and importlib.util.find_spec(n) is None]
_scb_missing
`)});
        return py;
      });
    const py = await ready;
    if (prepare !== undefined) {
      // A package that does not install shows up as an import error when the code runs.
      await py.loadPackagesFromImports(prepare).catch(() => {});
      if (packages.length > 0) {
        try {
          await install(py, packages);
        } catch (e) {
          return postMessage({ id, error: 'The packages did not install. ' + String(e?.message ?? e).trim().split('\\n').at(-1) });
        }
      }
      // Pure Python packages that Pyodide does not have come from PyPI, under their import name.
      const names = missing(prepare).toJs();
      if (names.length > 0) await install(py, names).catch(() => {});
      return postMessage({ id });
    }
    const decoder = new TextDecoder();
    let stdout = '';
    let stderr = '';
    py.setStdout({ write: (b) => ((stdout += decoder.decode(b, { stream: true })), b.length) });
    py.setStderr({ write: (b) => ((stderr += decoder.decode(b, { stream: true })), b.length) });
    const globals = py.globals.get('dict')();
    globals.set('__name__', '__main__');
    let failure;
    try {
      await runCode(code, globals, !!session, [file ?? 'main.py', ...args], columns, !!color);
    } catch (e) {
      failure = e;
    } finally {
      // Text after the last newline stays in Python's buffers until they flush.
      py.runPython('import sys; sys.stdout.flush(); sys.stderr.flush()');
      globals.destroy();
    }
    // Drop Pyodide's own frames, so that the traceback starts at the reader's code.
    if (failure) stderr += String(failure.message).replace(/^(Traceback[^\\n]*\\n)[\\s\\S]*?(?=  File "<exec>")/, '$1');
    postMessage({ id, stdout: stdout.replace(/\\n$/, ''), stderr: stderr.trimEnd() });
  } catch (e) {
    ready = undefined;
    postMessage({ id, error: String(e?.message ?? e) });
  }
};`;function n({url:n=e}={}){let r,i=0,a=new Map,o=new Map;function s(){let e=URL.createObjectURL(new Blob([t],{type:`text/javascript`})),n=new Worker(e,{type:`module`});return n.onmessage=({data:e})=>{let t=o.get(e.id);o.delete(e.id),e.error===void 0?t?.resolve(e):t?.reject(Error(e.error))},n.onerror=e=>{c();for(let t of o.values())t.reject(Error(e.message||`The worker did not start.`));o.clear()},n}function c(){r?.terminate(),r=void 0}function l(e,t){r??=s(),r.postMessage({id:e,url:new URL(n,globalThis.location?.href).href,...t})}function u(e,t){let n=o.get(e);if(n){o.delete(e),c(),n.reject(t);for(let[e,{message:t}]of o)`code`in t&&l(i++,{prepare:t.code,packages:t.packages}),l(e,t)}}function d(e,t){return new Promise((n,r)=>{if(t?.aborted)return r(t.reason);let a=i++;t?.addEventListener(`abort`,()=>u(a,t.reason),{once:!0}),o.set(a,{message:e,resolve:n,reject:r}),l(a,e)})}return{load:async(e,{packages:t=[]}={})=>{a.set(e,t),await d({prepare:e,packages:t})},run:async(e,{signal:t,session:n=!1,args:r,file:i,columns:o,color:s})=>{let{stdout:c=``,stderr:l=``}=await d({code:e,session:n,args:r,file:i,columns:o,color:s,packages:a.get(e)??[]},t);return{stdout:c,stderr:l}}}}var r=n();export{e as PYODIDE_URL,r as default,n as pyodide};