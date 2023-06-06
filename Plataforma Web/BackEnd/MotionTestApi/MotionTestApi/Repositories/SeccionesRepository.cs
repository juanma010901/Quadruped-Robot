using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Repositories
{
    public class SeccionesRepository: ControllerBase
    {
        private readonly EstadoContext _context;

        public SeccionesRepository(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }

        public async Task GuardarSecciones(Secciones seccion)
        {
            try
            {
                seccion.Fecha = DateTime.Now;
                _context.Add(seccion);

                await _context.SaveChangesAsync();
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
                _context.Secciones.Update(seccion);
                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Sección actualizado con exito" });
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
                List<Secciones> listaSecciones =  _context.Secciones.ToList();

                return listaSecciones;
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

    }
}
