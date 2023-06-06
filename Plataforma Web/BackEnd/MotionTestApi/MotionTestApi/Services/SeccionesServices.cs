using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using MotionTestApi.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Services
{
    public class SeccionesServices: ControllerBase
    {
        private readonly SeccionesRepository _seccionesRepository;

        public SeccionesServices(SeccionesRepository seccionesRepository)
        {
            _seccionesRepository = seccionesRepository;
        }

        public async Task GuardarSecciones(Secciones seccion)
        {
            try
            {
                await _seccionesRepository.GuardarSecciones(seccion);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarSeccion(Secciones seccion)
        {
            try
            {
                seccion.Fecha = DateTime.Now;
                await _seccionesRepository.ActualizarSeccion(seccion);

                return Ok(new { mensaje = "Seccion actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        public List<Secciones> GetSecciones()
        {
            try
            {
                return _seccionesRepository.GetSecciones();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


    }
}
