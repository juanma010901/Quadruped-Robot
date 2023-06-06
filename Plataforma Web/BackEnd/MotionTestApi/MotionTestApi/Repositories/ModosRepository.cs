using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Repositories
{
    public class ModosRepository: ControllerBase
    {
        private readonly EstadoContext _context;

        public ModosRepository(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }

        public async Task GuardarModo(Modos modos)
        {
            try
            {
                modos.Fecha = DateTime.Now;
                _context.Add(modos);

                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarModo(List<Modos> modos)
        {
            try
            {
                _context.Modos.UpdateRange(modos);
                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Modos actualizados con exito" });
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }


        public Modos GetModoActual()
        {
            try
            {
                return _context.Modos.Where(r => r.Activo == true).FirstOrDefault();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public List<Modos> GetModos()
        {
            try
            {
                return _context.Modos.ToList();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

    }
}
