using Microsoft.EntityFrameworkCore;
using MotionTestApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi
{
    public class EstadoContext : DbContext
    {
        public EstadoContext(DbContextOptions<EstadoContext> options)
        : base(options)
        { }

        public DbSet<Motion> Motion { get; set; }
        public DbSet<Track> Track { get; set; }
        public DbSet<Puntos> Puntos { get; set; }
        public DbSet<Modos> Modos { get; set; }
        public DbSet<Movimientos> Movimientos { get; set; }
        public DbSet<Secciones> Secciones { get; set; }
        public DbSet<Angulos> Angles { get; set; }
    }
}
