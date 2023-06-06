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
    public class PuntosController : ControllerBase
    {
        private readonly PuntosServices _puntosService;

        public PuntosController(PuntosServices puntosService)
        {
            _puntosService = puntosService;
        }

        [FunctionName("GuardarPuntos")]
        public async Task<IActionResult> GuardarPuntos(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Puntos puntos,
            ILogger log)
        {
            try
            {
                await _puntosService.GuardarPuntos(puntos);
                return Ok(new { mensaje = "Puntos almacenado con éxito" });
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

        [FunctionName("ActualizarPunto")]
        public async Task<IActionResult> ActualizarPunto(
            [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = null)][FromBody] Puntos punto,
            ILogger log)
        {
            try
            {
                await _puntosService.ActualizarPunto(punto);

                return Ok(new { mensaje = "Punto actualizado con exito" });
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

        [FunctionName("GetPuntosById")]
        public async Task<IActionResult> GetPuntosById(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "GetPuntosById/{puntoId}")] HttpRequest req, int puntoId)
        {

            List<Puntos> puntos =  _puntosService.GetPuntosById(puntoId);
            return Ok(puntos);

        }


    }
}
