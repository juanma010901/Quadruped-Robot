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
    public class AngulosController : ControllerBase
    {
        private readonly AngulosServices _angulosService;

        public AngulosController(AngulosServices angulosService)
        {
            _angulosService = angulosService;
        }

        [FunctionName("GuardarAngulos")]
        public async Task<IActionResult> GuardarAngulo(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Angulos angulos,
            ILogger log)
        {
            try
            {
                await _angulosService.GuardarAngulo(angulos);
                return Ok(new { mensaje = "Angulo almacenado con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("GetAngulos")]
        public List<Angulos> GetAngulos(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
            ILogger log)
        {

            return _angulosService.GetAngulos();

        }

        [FunctionName("DeleteAngulos")]
        public async Task<IActionResult> DeleteAngulos(
            [HttpTrigger(AuthorizationLevel.Anonymous, "delete", Route = null)][FromBody] HttpRequest req,
            ILogger log)
        {
            try
            {
                await _angulosService.DeleteAngulos();
                return Ok(new { mensaje = "Angulos eliminados con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

    }
}
