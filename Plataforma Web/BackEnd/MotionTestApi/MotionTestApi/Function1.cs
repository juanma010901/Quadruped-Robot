using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using MotionTestApi.Models;
using System.Linq;

namespace MotionTestApi
{
    public class Function1 : ControllerBase
    {
        private readonly EstadoContext _context;

        public Function1(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }


        [FunctionName("SaveMotion")]
        public async Task<IActionResult> SaveMotion(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)][FromBody] Motion motion,
            ILogger log)
        {
            try
            {
                _context.Add(motion);

                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Motion almacenado con éxito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("UpdateMotion")]
        public async Task<IActionResult> UpdateMotion(
        [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = null)][FromBody] Motion motion,
        ILogger log)
        {
            try
            {
                _context.Motion.Update(motion);
                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Motion actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        [FunctionName("GetMotion")]
        public IActionResult GetMotion(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "GetMotion")] HttpRequest req, 
        ILogger log)
        {
            try
            {
                var motion = _context.Motion.Where(r => r.Id == 1).FirstOrDefault();

                return Ok(motion);
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }
    }
}
