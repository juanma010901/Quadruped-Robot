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
    public class ModosController : ControllerBase
    {
        private readonly ModosServices _modosService;

        public ModosController(ModosServices modosService)
        {
            _modosService = modosService;
        }

        [FunctionName("GuardarModo")]
        public async Task<IActionResult> GuardarModo(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Modos modos,
            ILogger log)
        {
            try
            {
                await _modosService.GuardarModo(modos);
                return Ok(new { mensaje = "Modo almacenado con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("ActualizarModo")]
        public async Task<IActionResult> ActualizarModo(
            [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = null)][FromBody] Modos modo,
            ILogger log)
        {
            try
            {
                await _modosService.ActualizarModo(modo);

                return Ok(new { mensaje = "Punto actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("GetModoActual")]
        public Modos GetModoActual(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
                ILogger log)
        {

            return _modosService.GetModoActual();

        }

        [FunctionName("GetModos")]
        public List<Modos> GetModos(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
        ILogger log)
        {

            return _modosService.GetModos();

        }

    }
}
