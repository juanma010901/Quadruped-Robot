using iText.Forms.Xfdf;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using MotionTestApi.Models;
using MotionTestApi.Services;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Controllers
{
    public class SeccionesController : ControllerBase
    {
        private readonly SeccionesServices _seccionesService;

        public SeccionesController(SeccionesServices seccionesService)
        {
            _seccionesService = seccionesService;
        }

        [FunctionName("GuardarSecciones")]
        public async Task<IActionResult> GuardarSecciones(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Secciones seccion,
            ILogger log)
        {
            try
            {
                await _seccionesService.GuardarSecciones(seccion);
                return Ok(new { mensaje = "Puntos almacenado con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("ActualizarSeccion")]
        public async Task<IActionResult> ActualizarSeccion(
            [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = null)][FromBody] Secciones seccion,
            ILogger log)
        {
            try
            {
                await _seccionesService.ActualizarSeccion(seccion);

                return Ok(new { mensaje = "Sección actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        [FunctionName("GetSecciones")]
        public List<Secciones> GetSecciones(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
                ILogger log)
        {

            return _seccionesService.GetSecciones();

        }

    }
}
