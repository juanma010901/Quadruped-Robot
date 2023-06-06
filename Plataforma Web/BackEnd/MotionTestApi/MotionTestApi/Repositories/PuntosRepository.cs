using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Repositories
{
    public class PuntosRepository: ControllerBase
    {
        private readonly EstadoContext _context;

        public PuntosRepository(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }

        public async Task GuardarPuntos(Puntos puntos)
        {
            try
            {
                puntos.Fecha = DateTime.Now;
                _context.Add(puntos);

                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarPunto(Puntos punto)
        {
            try
            {
                _context.Puntos.Update(punto);
                await _context.SaveChangesAsync();

                return Ok(new { mensaje = "Punto actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public List<Puntos> GetPuntosByIds(List<int> puntos)
        {
            try
            {
                List<Puntos> listaPuntos =  _context.Puntos.Where(r => puntos.Contains(r.Id)).ToList();

                return listaPuntos;
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

        public List<Puntos> GetPuntosById(int puntoId)
        {
            try
            {
                List<Puntos> listaPuntos = _context.Puntos.Where(r => r.Id == puntoId).ToList();

                return listaPuntos;
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

    }
}
