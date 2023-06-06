using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Repositories
{
    public class MovimientosRepository: ControllerBase
    {
        private readonly EstadoContext _context;

        public MovimientosRepository(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }

        public async Task GuardarMovimiento(Movimientos movimiento)
        {
            try
            {
                movimiento.Fecha = DateTime.Now;
                _context.Add(movimiento);

                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarMovimiento(Movimientos movimiento)
        {
            try
            {
                _context.Movimientos.Update(movimiento);
                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Movimiento actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public List<int> GetMovimientosByModoId(int modoId)
        {
            try
            {
                List<int> listaMovimientos = _context.Movimientos.Where(r => r.ModoId == modoId).Select(r => r.PuntosId).ToList();

                return listaMovimientos;
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

    }
}
