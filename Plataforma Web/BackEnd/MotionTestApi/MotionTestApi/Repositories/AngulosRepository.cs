using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Repositories
{
    public class AngulosRepository: ControllerBase
    {
        private readonly EstadoContext _context;

        public AngulosRepository(EstadoContext dbcontext)
        {
            _context = dbcontext;
        }

        public async Task GuardarAngulo(Angulos angulos)
        {
            try
            {
                angulos.Fecha = DateTime.Now;
                _context.Add(angulos);

                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public List<Angulos> GetAngulos()
        {
            try
            {
                return _context.Angles.ToList();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task DeleteAngulos()
        {
            try
            {
                var query = "DELETE FROM Angles; DBCC CHECKIDENT('Angles', RESEED, 0)";
                await _context.Database.ExecuteSqlRawAsync(query);
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

    }
}
