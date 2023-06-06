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
    public class MovimientosServices: ControllerBase
    {
        private readonly MovimientosRepository _movimientosRepository;
        private readonly PuntosServices _puntosServices;
        private readonly ModosServices _modosServices;

        public MovimientosServices(MovimientosRepository movimientosRepository, PuntosServices puntosServices, ModosServices modosServices)
        {
            _movimientosRepository = movimientosRepository;
            _puntosServices = puntosServices;
            _modosServices = modosServices;
        }

        public async Task GuardarMovimiento(Movimientos movimiento)
        {
            try
            {
                await _movimientosRepository.GuardarMovimiento(movimiento);
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
                movimiento.Fecha = DateTime.Now;
                await _movimientosRepository.ActualizarMovimiento(movimiento);

                return Ok(new { mensaje = "Movimiento actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        public List<Puntos> GetMovimientosByModoId()
        {
            try
            {
                int modoId = _modosServices.GetModoActual().Id;
                List<int> puntosId = _movimientosRepository.GetMovimientosByModoId(modoId);

                List<Puntos> puntos = _puntosServices.GetPuntosByIds(puntosId);

                return puntos;
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


    }
}
