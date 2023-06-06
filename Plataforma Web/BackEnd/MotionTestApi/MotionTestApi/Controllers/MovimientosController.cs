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
    public class MovimientosController : ControllerBase
    {
        private readonly MovimientosServices _movimientosService;

        public MovimientosController(MovimientosServices movimientosService)
        {
            _movimientosService = movimientosService;
        }

        [FunctionName("GuardarMovimiento")]
        public async Task<IActionResult> GuardarMovimiento(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Movimientos movimiento,
            ILogger log)
        {
            try
            {
                await _movimientosService.GuardarMovimiento(movimiento);
                return Ok(new { mensaje = "Movimiento almacenado con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("ActualizarMovimiento")]
        public async Task<IActionResult> ActualizarMovimiento(
            [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = null)][FromBody] Movimientos movimiento,
            ILogger log)
        {
            try
            {
                await _movimientosService.ActualizarMovimiento(movimiento);

                return Ok(new { mensaje = "Movimiento actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        [FunctionName("GetPuntos")]
        public List<Puntos> GetMovimientosByModoId(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
        ILogger log)
        {

            return _movimientosService.GetMovimientosByModoId();

        }




    }
}
